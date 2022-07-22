import random
import time

import paho.mqtt.client as mqtt



def on_connect(client, userdata, flags, rc):
	
	if rc == 0:
	
		print("Connected to MQTT Broker!")
		
	else:
	
		print('Failed to connect, return code {:d}'.format(rc))



def on_message(client, userdata, msg):
	
	print('Received {} from {} topic'.format(msg.payload.decode(), msg.topic))



def run():

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



if __name__ == '__main__':
	
	run()