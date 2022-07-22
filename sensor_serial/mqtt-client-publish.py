import random
import time

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to MQTT Broker!")
	else:
		print('Failed to connect, return code {:d}'.format(rc))


def run():
	try:
		broker = 'broker.emqx.io'
		port = 1883
		topic = "/sws3025/lecture07"
		client_id = f'python-mqtt-{random.randint(0, 10000)}'
		username = 'emqx'
		password = 'public'

		print('client_id={}'.format(client_id))


		# Set Connecting Client ID
		client = mqtt.Client(client_id)
		client.username_pw_set(username, password)
		client.on_connect = on_connect
		client.connect(broker, port)

		client.loop_start()
		
		msg_count = 0
		
		while True:
		
			time.sleep(1)
			
			msg = f'messages: {msg_count}'
			result = client.publish(topic, msg)
			# result: [0, 1]
			status = result[0]
			
			if status == 0:
			
				print('Send {} to topic {}'.format(msg, topic))
				
			else:
			
				print('Failed to send message to topic {}'.format(topic))
			
			msg_count += 1

	except KeyboardInterrupt:

			print('Program terminated!')



if __name__ == '__main__':
	
	run()
