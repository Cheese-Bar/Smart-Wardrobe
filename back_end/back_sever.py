import json
from flask import Flask, request,  redirect, render_template,session
import sqlite3
from flasgger import Swagger
from flask_cors import CORS, cross_origin #导入包
import requests
import random
import numpy as np
from predict import predict_temp, temp_to_cloth

app = Flask(__name__)
Swagger(app)
CORS(app, supports_credentials=True)#设置参数
# app.secret_key='QWERTYUIOP'#对用户信息加密


def upload(img):
	res = ''
	try:
		headers = {'Authorization': 'NOCejrcI6d8eJNtWDShKuNDAcXlJ4gFV'}
		url = 'https://sm.ms/api/v2/upload'
		print(img)
		res = requests.post(url, files=img, headers=headers).json()
		print(res)
		return res['data']['url']
	except Exception as e:
		print(e)
		return res['images']

@app.route('/login',methods=['GET',"POST"])#路由默认接收请求方式位POST，然而登录所需要请求都有，所以要特别声明。
def login():
	if request.method=='GET':
		return  render_template('login.html')
	user=request.form.get('user')
	pwd=request.form.get('pwd')
	if user=='admin' and pwd=='123':#这里可以根据数据库里的用户和密码来判断，因为是最简单的登录界面，数据库学的不是很好，所有没用。
		session['user_info']=user
		return redirect('/index')
	else:
		return  render_template('login.html',msg='用户名或密码输入错误')
 
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

	return json.dumps(res)


@app.route('/getHistory')
def getHistory():
	"""
	获得历史的室外数据
	[24] + [24] + [24] + (1) 暂未实现
    ---
    responses:
      500:
        description: Error
      200:
        description: 室外历史数据
    """

	conn = sqlite3.connect('../database/smart_wardrobe.db')
	cur = conn.cursor()
	sql = '''select temp, humidity, pressure
			from (
					select *
					from outdoor

					order by time desc
					limit 24
				)
			order by time'''
		# where temp and humidity and pressure is not null
	result = cur.execute(sql).fetchall()
	result = np.array(result)
	temp_list = list(result[:,0])
	humi_list = list(result[:,1])
	pres_list = list(result[:,2])
	re = {'temp_list': temp_list,
			'humi_list': humi_list,
			'pres_list': pres_list}
	return json.dumps(re)

@app.route('/uploadImage', methods=['POST'])
def uploadImg():
	name = request.form.get('name')
	img = request.files.get('upload')
	print({'smfile':img})
	url = upload({'smfile':img})
	conn = sqlite3.connect('../database/smart_wardrobe.db')
	cur = conn.cursor()

	cloth_type = 0
	# TODO: 需要添加识别

	try:
		sql = '''insert into images (name, url, type) values(?,?,?)'''
		cur.execute(sql, (name, url, cloth_type))
		conn.commit()
		print("插入图片成功")
		cur.close()
		conn.close()
		return "插入图片成功"
	except Exception as e:
		print(e)
		conn.rollback()
		cur.close()
		conn.close()
		return "存在同名衣服或其他错误"

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
	sql = '''select id, name, url from images'''
	result = cur.execute(sql).fetchall()
	re = {'all':[]}
	for item in result:
		re['all'].append({'id': item[0],'name':item[1], 'url':item[2]})
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
	sql = '''select temp
				from (
					select *
					from outdoor
					where temp is not null
					order by time desc
					limit 24)
				order by time'''
	temp_list = cur.execute(sql).fetchall()
	temp_list = np.array(temp_list)[:,0]
	print(temp_list)
	p_temp = predict_temp(temp_list)
	print(p_temp)
	# TODO: 根据温度-衣服模型获得合适的type
	c_type = temp_to_cloth(p_temp)
	# TODO: 根据type 挑选一件合适的衣服

	sql = '''select name, url from images
	where type = ?'''
	result = cur.execute(sql, (c_type,)).fetchall()
	cur.close()
	conn.close()

	if result: 
		re = {'bestfit': result[random.randint(0,len(result)-1)]}
		return json.dumps(re)
	return '当前没有合适的衣服捏， 快去添加新衣服叭~'

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
		return '删除成功'
	except Exception as e:
		print(e)
		conn.rollback()
		cur.close()
		conn.close()
		return '删除失败'
	
if __name__ == '__main__':
	# upload({'smfile': open('../images/mianao2.jpg', 'rb')})
	try:
		app.run('0.0.0.0',9000, debug=True)
	except:
		print('Program terminated!')
