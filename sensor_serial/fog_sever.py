from pip import main
from threading import Thread

import serial
import time
import random
import paho.mqtt.client as mqtt
from queue import Queue


def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to MQTT Broker!")
	else:
		print('Failed to connect, return code {:d}'.format(rc))

def fog_publish(queue):
	
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
    client.loop_start()
    
    msg_count = 0
    
    while True:
        if queue.empty() == False:
            temp_msg = queue.get()
            # print(temp_msg)
            msg = '{} | {}: {}'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),temp_msg[0],temp_msg[1])
            result = client.publish(topic, msg)
            status = result[0]
            
            if status == 0:
                print('Send {} to topic {}'.format(msg, topic))
            else:
                print('Failed to send message to topic {}'.format(topic))
            msg_count += 1
            time.sleep(1)



def fog_recv_serial(queue):
    try:
        print("Listening on /dev/ttyACM0... Press CTRL+C to exit")
        ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
        
        while True:
            msg = ser.readline()
            smsg = msg.decode('utf-8').strip()

            if len(smsg) > 0:
                print('{}'.format(smsg))
                queue.put((smsg.split(':')[0],smsg.split(':')[1]))
            time.sleep(1)

    except KeyboardInterrupt:
        if ser.is_open:
            ser.close()
        print("Program terminated!")

if __name__=='__main__':
    queue = Queue()

    try:
        t1 = Thread(target=fog_recv_serial, args=(queue, ))
        t2 = Thread(target=fog_publish, args=(queue, ))

        t1.start()
        t2.start()

        t1.join()  
        t2.join()
    except:
        print('End')


