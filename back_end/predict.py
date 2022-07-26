import tensorflow as tf
import pandas as pd
import numpy as np

def predict_temp(data):
    final_model = tf.keras.models.load_model("./model/test_model.hdf5",compile=True)
    pred = final_model.predict(data)
    return pred

def temp_to_cloth(temp):
    type = 0
    return type

