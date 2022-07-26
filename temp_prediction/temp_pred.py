import tensorflow as tf
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score
from tensorflow.keras import utils,losses,layers,Sequential
from tensorflow.keras.callbacks import ModelCheckpoint,TensorBoard
import sqlite3

def multivariate_data(x,y, start_index, end_index, history_size,
                      target_size, step, single_step):

    #single_step意思是只预测目标的一个未来状态，只预测后1小时，设置为false可以预测未来0到target_size小时内的温度。
    data = []
    labels = []

    start_index = start_index + history_size
    
    if end_index is None:
        end_index = len(dataset) - target_size

    for i in range(start_index, end_index):
        indices = range(i-history_size, i, step) # step表示滑动步长
        mid_data=x.iloc[indices]
        data.append(mid_data)

        if single_step:
            mid_data=y.iloc[i+target_size]
            labels.append(mid_data)
        else:
            labels.append(y.iloc[i:i+target_size])

    return np.array(data), np.array(labels)

def create_batch_dataset(x,y,train=True,buffer_size=1000,batch_size=128):
    batch_data=tf.data.Dataset.from_tensor_slices((tf.constant(x),tf.constant(y)))
    if train:
        return batch_data.cache().shuffle(buffer_size).batch(batch_size)
    else:
        return batch_data.batch(batch_size)

data_path="./beijing2.csv"
dataset=pd.read_csv(data_path, parse_dates=["dates"],index_col=False)
dataset=dataset.set_index(dataset.columns[0])
# dataset=pd.read_csv(data_path)

df=dataset[['T','Po','U']]
df=dataset[['T','Po','U']]
df.columns=['Temp','pressure','Humidity']
df['month']=df.index.month
df['hour']=df.index.hour
df['sin(h)']=[np.sin((x) * (2 * np.pi / 24)) for x in df['hour']]
df['cos(h)']=[np.cos((x) * (2 * np.pi / 24)) for x in df['hour']]

future=['sin(h)','cos(h)','month','Temp','pressure','Humidity']
#数据归一化，由于sin和cos本来就是-1到1，不用归一化
for col in future:
    scaler=MinMaxScaler()
    if(col not in ['sin(h)','cos(h)']):
    	dataset[col]=scaler.fit_transform(dataset[col].values.reshape(-1,1))

x=df[future]
y=df['Temp']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,shuffle=False,random_state=13)



#取得训练集，和测试集的格式
train_dataset,train_labels=multivariate_data(x_train,y_train,0,None,24,1,1,False)
test_dataset,test_labels=multivariate_data(x_test,y_test,0,None,24,1,1,False)
print(test_dataset)

train_batch_dataset=create_batch_dataset(train_dataset,train_labels)
test_batch_dataset=create_batch_dataset(test_dataset,test_labels,train=False)

model= tf.keras.models.Sequential([
    tf.keras.layers.LSTM(256, input_shape=train_dataset.shape[-2:],return_sequences=True), # input_shape=(20,1) 不包含批处理维度
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.LSTM(128, return_sequences=True),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.LSTM(32),
    tf.keras.layers.Dense(1)
])

#优化器和损失函数设置
model.compile(optimizer='adam',loss='mse')

#模型保存的相关设置
utils.plot_model(model)
checkpoint_file= 'test_model_gooood.hdf5'
checkpoint_callback=ModelCheckpoint(filepath=checkpoint_file,monitor='loss',moode='min',save_best_only=True,save_weights_only=True)
#模型训练
history=model.fit(train_batch_dataset,epochs=30,validation_data=test_batch_dataset,callbacks=[checkpoint_callback])

plt.figure(figsize=(8,8),dpi=200)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model train vs validation loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train','validation'], loc='best')
plt.show()


test_preds=model.predict(test_dataset,verbose=1)
test_preds=test_preds[:,0]
score=r2_score(test_labels,test_preds)
print(score)

plt.figure(figsize=(16,8))
plt.plot(test_labels[:1000],label="True value")
plt.plot(test_preds[:1000],label="Pred value")
plt.legend(loc='best')
plt.show()