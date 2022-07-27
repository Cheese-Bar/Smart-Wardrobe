from sqlite3 import DatabaseError
import tensorflow as tf
import pandas as pd
import numpy as np
import pickle
import PIL
import PIL.ImageOps
from PIL import Image
from io import BytesIO
from werkzeug.datastructures import FileStorage
from sklearn.preprocessing import MinMaxScaler
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

def predict_temp(data):
    print(data)
    # final_model = tf.keras.models.load_model("./model/test_model.hdf5",compile=True)
    final_model = tf.keras.models.load_model("./model/test_model_gooood.hdf5",compile=True)
    # data = np.array(data, dtype='float32')
    df = pd.DataFrame(data)
    df.columns=['time','temp', 'humidity', 'pressure']
    df=df.set_index(df.columns[0])
    df.index = pd.to_datetime(df.index)
    df['month']=df.index.month
    df['hour']=df.index.hour
    df['sin(h)']=[np.sin((x) * (2 * np.pi / 24)) for x in df['hour']]
    df['cos(h)']=[np.cos((x) * (2 * np.pi / 24)) for x in df['hour']]
    future=['sin(h)','cos(h)','month','temp','pressure','humidity']
    # 气压转化为毫米汞柱
    df['pressure'] = df['pressure']*0.0075
    #数据归一化，由于sin和cos本来就是-1到1，不用归一化
    for col in future:
        scaler=MinMaxScaler()
        if(col not in ['sin(h)','cos(h)']):
            df[col]=scaler.fit_transform(df[col].values.reshape(-1,1))
    x=np.array([np.array(df[future])])
    # print(x,x.shape)

    pred = final_model.predict(x)
    pred = scaler.inverse_transform(pred)
    print('预测温度',pred)
    return pred

def temp_to_cloth(temp):
    with open('./model/svc.pickle','rb') as f:
        model = pickle.load(f)
        c_type = model.predict(temp)
        print(c_type)
    return newindex(c_type)

def newindex(n):
	if n == 0:
		return "a T-SHIRT/TOP"
	elif n == 1:
		return "shirt"
	elif n == 3:
		return "a PULLOVER"
	elif n == 4:
		return "a COAT"
	else:
		return "Unknown"

def cloth_recognition(imgArray):
    # BytesIO(imgArray).save('./temp')
    # img = open('./temp','rb')
    img = PIL.Image.open(BytesIO(imgArray)).convert("L")
    # img = PIL.Image.open("img/" + 'pullover.jpg').convert("L")
    img = img.resize((28, 28), Image.ANTIALIAS)
    img = PIL.ImageOps.invert(img)
    img = np.array(img)


    img = np.array(img).reshape(1,28,28,1)
    new_model = tf.keras.models.load_model("./model/smartwardrobe2.model".encode("utf-8"))
    prediction = new_model.predict(img)
    print(prediction)
    return newindex(np.argmax(prediction))