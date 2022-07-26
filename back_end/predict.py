import tensorflow as tf
import pandas as pd
import numpy as np
import pickle

def predict_temp(data):
    final_model = tf.keras.models.load_model("./model/test_model.hdf5",compile=True)
    pred = final_model.predict(data)
    return pred

def temp_to_cloth(temp):
    with open('./model/svc.pickle','rb') as f:
        model = pickle.load(f)
        c_type = model.predict([[temp]])
        print(c_type)
    return c_type

