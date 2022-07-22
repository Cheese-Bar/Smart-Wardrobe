
import random
import time
import sqlite3

from threading import Thread

import paho.mqtt.client as mqtt
from queue import Queue

def trans_key(key):
	if key == 'Otemp': 
		return 'outdoor', 'temp'
	elif key == 'Ohumidity': 
		return 'outdoor', 'humidity'
	elif key == 'Itemp': 
		return 'indoor', 'temp'
	elif key == 'Ihumidity': 
		return 'indoor', 'humidity'

def database_exe(conn, time, key, value):
	flag, key = trans_key(key)
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

def pc_insert_data(queue,conn):
	while True:
		if queue.empty()==False:
			temp_msg = queue.get()
			time = temp_msg.split('|')[0]
			key, value = temp_msg.split('|')[1].split(':')[0], temp_msg.split('|')[1].split(':')[1]
			database_exe(conn, flag, time, key, value)


if __name__ == '__main__':
	conn = sqlite3.connect('smart_wardrobe.db')
	queue = Queue()
	# pc_subscribe(queue)
	try:
		t1 = Thread(target=pc_subscribe, args=(queue,))
		t2 = Thread(target=pc_insert_data, args=(queue, conn))		
		t1.start()
		t2.start()
		t1.join()
		t2.join()
	except:
		conn.close()
		print('End')