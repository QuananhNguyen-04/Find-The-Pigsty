import pandas as pd
import numpy as np
import tensorflow as tf
import keras
import os

file = open("./state.data", 'r')

data = pd.read_csv(file)
file.close()

data = data.to_numpy(dtype='float16')

value = data[:, 10]
state = data[:, :4]

if any(num == np.nan for num in value):
    raise Exception("Loss Function Error")
    os.__exit(0)

# model = tf.keras.models.Sequential([
#     tf.keras.layers.Flatten(input_shape=(4,)),
#     tf.keras.layers.Dense(32, 'tanh'),
#     tf.keras.layers.Dense(32, 'tanh'),
#     tf.keras.layers.Dense(16, 'tanh'),
#     tf.keras.layers.Dense(4, activity_regularizer='L2')
# ])

# model.compile('adam', loss='mae')
# model.fit(state, value,epochs=70)

model = tf.keras.models.load_model("rein.keras")
model.fit(state, value, epochs = 30)
model.save("rein.keras")