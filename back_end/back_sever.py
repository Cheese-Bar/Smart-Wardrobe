import json
from re import T
from unittest import result

from matplotlib.pyplot import axis
from flask import Flask, request,  redirect, render_template,session
import sqlite3
from flasgger import Swagger
from flask_cors import CORS, cross_origin #导入包
import requests
import random
import numpy as np
from predict import predict_temp, temp_to_cloth, cloth_recognition


import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

app = Flask(__name__)
Swagger(app)
CORS(app, supports_credentials=True)#设置参数
# app.secret_key='QWERTYUIOP'#对用户信息加密


def upload(img):
	res = ''
	try:
		headers = {'Authorization': 'NOCejrcI6d8eJNtWDShKuNDAcXlJ4gFV'}
		url = 'https://sm.ms/api/v2/upload'
		res = requests.post(url, files=img, headers=headers).json()
		print(res)
		res = res['data']['url']
		print('上传图床成功, URL:'+res)
		return res
	except Exception as e:
		print('上传图床失败')
		print(e)
		return res['images']

@app.route('/getRealData')
def getRealData():
	# parameters:
    #   - name: language
    #     in: path
    #     type: string
    #     required: true
    #     description: The language name
    #   - name: size
    #     in: query
    #     type: integer
    #     description: size of awesomeness

	"""
	获得最新的室内外数据
    ---
    responses:
      500:
        description: Error
      200:
        description: 室内外数据
    """
	conn = sqlite3.connect('../database/smart_wardrobe.db')
	cur = conn.cursor()

	sql1 = '''select time, temp, humidity, pressure from outdoor 
	where temp not null and humidity not null and pressure not null 
	order by id desc 
	limit 1'''
	result1 = cur.execute(sql1)
	result1 = result1.fetchall()

	sql2 = '''select time, temp, humidity from indoor 
	where temp not null and humidity not null  
	order by id desc 
	limit 1'''
	result2 = cur.execute(sql2)
	result2 = result2.fetchall()

	cur.close()
	conn.close()
	
	res = {'outdoor':{}, 'indoor':{}}
	res['outdoor']['time'] = result1[0][0]
	res['outdoor']['temp'] = result1[0][1]
	res['outdoor']['humidity'] = result1[0][2]
	res['outdoor']['pressure'] = result1[0][3]
	res['indoor']['time'] = result2[0][0]
	res['indoor']['temp'] = result2[0][1]
	res['indoor']['humidity'] = result2[0][2]
	res['statu'] = 'success'

	return json.dumps(res)

@app.route('/getHistory')
def getHistory():
	"""
	获得历史的室外数据
	[24] + [24] + [24] + (1) 已实现
    ---
    responses:
      500:
        description: Error
      200:
        description: 室外历史数据
    """

	conn = sqlite3.connect('../database/smart_wardrobe.db')
	cur = conn.cursor()
	sql = '''select time, temp, humidity, pressure
			from (
					select *
					from outdoor
					where temp and humidity and pressure is not null
					order by id desc
					limit 24
				)
			order by id'''
		# where temp and humidity and pressure is not null
	result = cur.execute(sql).fetchall()
	p_temp = predict_temp(result)
	result = np.array(result)
	# temp_list = list(np.concatenate((result[:,1],(np.array(p_temp[0][0], dtype='float32')))))
	temp_list = list(result[:,1])
	temp_list = [float(x) for x in temp_list]
	temp_list.append(float(str(p_temp[0][0])))
	# print (type(temp_list), len(temp_list),type(p_temp))
	# temp_list = temp_list.append(p_temp[0][0])
	humi_list = list(result[:,2])
	pres_list = list(result[:,3])
	# temp_list.append(p_temp)
	print(temp_list)
	re = {'temp_list': temp_list,
			'humi_list': humi_list,
			'pres_list': pres_list,
			'pred_temp': '{:.2f}'.format(float(p_temp[0][0]))}
	re['statu'] = 'success'
	return json.dumps(re)

@app.route('/uploadImage', methods=['POST'])
def uploadImg():
	name = request.form.get('name')
	img = request.files.get('upload')
	img = img.read()
	# print('log',{'smfile':img})
	url = upload({'smfile':img})
	conn = sqlite3.connect('../database/smart_wardrobe.db')
	cur = conn.cursor()

	cloth_type = 0
	# TODO: 需要添加识别
	cloth_type = cloth_recognition(img)

	try:
		sql = '''insert into images (name, url, type) values(?,?,?)'''
		cur.execute(sql, (name, url, cloth_type))
		conn.commit()
		print("插入图片成功")
		cur.close()
		conn.close()
		return json.dumps({'statu': 'success','msg':'图片已录入数据库'})
	except Exception as e:
		print(e)
		conn.rollback()
		cur.close()
		conn.close()
		print("图片插入数据库失败,请检查是否重名")
		return json.dumps({'statu': 'fail','msg':'名称已经存在'})

@app.route('/getAll')
def getAll():
	"""
	得到所有的衣橱数据
    ---
    responses:
      500:
        description: Error
      200:
        description: 得到所有数据
    """
	conn = sqlite3.connect('../database/smart_wardrobe.db')
	cur = conn.cursor()
	sql = '''select id, name, url, type from images'''
	result = cur.execute(sql).fetchall()
	re = {'statu':'','all':[]}
	if result:
		for item in result:
			re['all'].append({'id': item[0],'name':item[1], 'url':item[2], 'type':item[3]})
		re['statu'] = 'success'
	else:
		re['statu'] = 'fail'
	return json.dumps(re)

@app.route('/getBestFit')
def getBest():
	"""
	得到推荐的衣物
    ---
    responses:
      500:
        description: Error
      200:
        description: 得到推荐的衣物 {bestfit:[name,url]}
    """
	conn = sqlite3.connect('../database/smart_wardrobe.db')
	cur = conn.cursor()
	# TODO: 获得预测的温度
	# sql = '''select temp
	# 			from (
	# 				select *
	# 				from outdoor
	# 				where temp is not null
	# 				order by time desc
	# 				limit 24)
	# 			order by time'''
	# temp_list = cur.execute(sql).fetchall()
	# temp_list = np.array(temp_list)[:,0]
	sql = '''select time, temp, humidity, pressure
			from (
					select *
					from outdoor
					where temp and humidity and pressure is not null
					order by id desc
					limit 24
				)
			order by id'''

	history = cur.execute(sql).fetchall()
	p_temp = predict_temp(history)
	print(p_temp)
	# TODO: 根据温度-衣服模型获得合适的type
	c_type = temp_to_cloth(p_temp)
	# TODO: 根据type 挑选一件合适的衣服
	print(c_type)

	sql = '''select name, url, type from images
	where type = ?'''
	result = cur.execute(sql, (c_type,)).fetchall()
	cur.close()
	conn.close()

	if result: 
		re = {'bestfit': result[random.randint(0,len(result)-1)], 'statu':'success'}
		return json.dumps(re)
	return json.dumps({'statu':'fail','msg':'当前没有合适的衣服捏， 快去添加新衣服叭~'})

@app.route('/deleteImage/<id>')
def delImag(id):
	conn = sqlite3.connect('../database/smart_wardrobe.db')
	cur = conn.cursor()
	sql = '''delete from images 
	where id = ?'''
	try:
		cur.execute(sql,(id,))
		conn.commit()
		cur.close()
		conn.close()
		return json.dumps({'statu': 'success', 'message':'删除成功'})
	except Exception as e:
		print(e)
		conn.rollback()
		cur.close()
		conn.close()
		return json.dumps({'statu': 'success', 'message':'删除失败'})
	
if __name__ == '__main__':
	# upload({'smfile': open('../images/mianao2.jpg', 'rb')})
	try:
		app.run('0.0.0.0',9000, debug=True)
	except:
		print('Program terminated!')
