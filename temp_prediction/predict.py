import tensorflow as tf
import pandas as pd
import numpy as np

final_model = tf.keras.models.load_model("test_model.hdf5",compile=True)
data = pd.read_json()
pred = final_model.predict(data)
print(data)