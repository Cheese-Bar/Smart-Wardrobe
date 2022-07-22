
import random
import re
import time
import sqlite3

from threading import Thread
from tkinter.messagebox import NO

import paho.mqtt.client as mqtt
from queue import Queue

def trans_key(key):
	key = key.strip()
	if key == 'Otemp': 
		return 'outdoor', 'temp'
	elif key == 'Ohumidity': 
		return 'outdoor', 'humidity'
	elif key == 'Opressure':
		return 'outdoor', 'pressure'
	elif key == 'Itemp': 
		return 'indoor', 'temp'
	elif key == 'Ihumidity': 
		return 'indoor', 'humidity'
	else:
		print('Wrong key! :{}'.format(key))
		return None, None

def database_exe(conn, time, key, value):
	flag, key = trans_key(key)
	if flag != None:
		cur = conn.cursor()
		sql = 'insert into {}(time, {}) values(?,?)'.format(flag, key) 
		try:
			cur.execute(sql,(time, value)) #插入一条数据
			conn.commit()
			print("插入数据成功")
		except Exception as e:
			print(e)
			conn.rollback()
			cur.close()
			print("插入数据失败")

	 
def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to MQTT Broker!")
	else:
		print('Failed to connect, return code {:d}'.format(rc))

def on_message(client, userdata, msg):
	print('Received {} from {} topic'.format(msg.payload.decode(), msg.topic))
	queue.put(msg.payload.decode())

def pc_subscribe(queen):
	try:
		broker = 'broker.emqx.io'
		port = 1883
		topic = "/SmartWardrobe/sensorData"
		client_id = f'python-mqtt-{random.randint(0, 10000)}'
		username = 'emqx'
		password = 'public'

		print('client_id={}'.format(client_id))

		# Set Connecting Client ID
		client = mqtt.Client(client_id)
		client.username_pw_set(username, password)
		client.on_connect = on_connect
		client.connect(broker, port)
		
		client.subscribe(topic)
		client.on_message = on_message

		client.loop_forever()				

	except KeyboardInterrupt:
			print('Program terminated!')

def pc_insert_data(queue,):
	conn = sqlite3.connect('smart_wardrobe.db')
	try:
		while True:
			if queue.empty()==False:
				temp_msg = queue.get()
				rec_time = temp_msg.split('|')[0]
				key, value = temp_msg.split('|')[1].split(':')[0], temp_msg.split('|')[1].split(':')[1]
				database_exe(conn, rec_time, key, value)
			time.sleep(1)
	except KeyboardInterrupt:
		print('Program terminated!')

if __name__ == '__main__':
	queue = Queue()
	try:
		t1 = Thread(target=pc_subscribe, args=(queue,))
		t2 = Thread(target=pc_insert_data, args=(queue,))		
		t1.start()
		t2.start()
		t1.join()
		t2.join()
	except KeyboardInterrupt:
		print('Program terminated!')