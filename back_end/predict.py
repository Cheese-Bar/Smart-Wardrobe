from sqlite3 import DatabaseError
import tensorflow as tf
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler

def predict_temp(data):
    print(data)
    final_model = tf.keras.models.load_model("./model/test_model.hdf5",compile=True)
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
    #数据归一化，由于sin和cos本来就是-1到1，不用归一化
    for col in future:
        scaler=MinMaxScaler()
        if(col not in ['sin(h)','cos(h)']):
            df[col]=scaler.fit_transform(df[col].values.reshape(-1,1))
    x=np.array([np.array(df[future])])
    # print(x,x.shape)

    pred = final_model.predict(x)
    print('预测温度',pred)
    return pred

def temp_to_cloth(temp):
    with open('./model/svc.pickle','rb') as f:
        model = pickle.load(f)
        c_type = model.predict([[temp]])
        print(c_type)
    return c_type

