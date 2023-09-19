from tensorflow import convert_to_tensor
from tensorflow.keras import models
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from  matplotlib.colors import LinearSegmentedColormap

cmap=LinearSegmentedColormap.from_list('rg',["r", "y", "g"], N=256) 
model = models.load_model("rein.keras")
x_pos = 350
y_pos = 200

data = []
for y in range(-150, 150, 10):
    temp = []
    for x in range(-150, 150, 10):
        input_tensor = convert_to_tensor(np.array([[x, y]], dtype='float16'))
        outputY = np.array(model.call(input_tensor))
        outputY = np.reshape(outputY, (-1))
        value = np.max(outputY)
        temp.append(value)
    data.append(temp)

data = np.array(data)

sns.heatmap(data=data, cmap=cmap)
plt.xlabel('x')
plt.ylim(0, 60)
plt.xlim(0, 60)
plt.ylabel('y')

plt.show()
