import imp
import requests
import json

    
img_str = {'upload':open( '../images/shirt.jpg', 'rb')}
res=requests.request("POST",'http://10.24.239.172:9000/uploadImage',data={'name':'test99'},files=img_str)