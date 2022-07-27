from picamera import PiCamera
from gpiozero import Button
from time import sleep
import imp
import requests
import json
import time

button = Button(14)
camera = PiCamera()

camera.start_preview()
frame = 1
while True:
    try:
        button.wait_for_press()
        sleep(2.5)
        camera.capture('./temp_imgs/frame%03d.jpg' % frame)
        img_str = {'upload':open('./temp_imgs/frame%03d.jpg' % frame, 'rb')}
        res=requests.request("POST",'http://192.168.155.197:9000/uploadImage',data={'name':'raspicamera{}.jpg' % time.time()}, files=img_str)

        frame += 1
    except KeyboardInterrupt:
        camera.stop_preview()
        break
