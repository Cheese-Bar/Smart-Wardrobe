from picamera import PiCamera
from gpiozero import Button
from time import sleep
import imp
import requests
import json


button = Button(14)
camera = PiCamera()

camera.start_preview()
frame = 1
while True:
    try:
        button.wait_for_press()
        sleep(5)
        fig = camera.capture('./temp_imgs/frame%03d.jpg' % frame)
    
        img_str = {'upload':fig}
        res=requests.request("POST",'http://10.24.239.172:9000/uploadImage',data={'name':'frame%03d.jpg' % frame}, files=img_str)

        frame += 1
    except KeyboardInterrupt:
        camera.stop_preview()
        break
