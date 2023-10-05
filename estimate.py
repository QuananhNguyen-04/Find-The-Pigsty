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
direct = []
for y in range(-150, 150, 10):
    temp = []
    temp_dir = []
    for x in range(-150, 150, 10):
        input_tensor = convert_to_tensor(np.array([[x, y, x - 50, x + 50]], dtype='float16'))
        outputY = np.array(model.call(input_tensor))
        outputY = np.reshape(outputY, (-1))
        value = np.max(outputY)
        temp.append(value)
        temp_dir.append(np.argmax(outputY))
    data.append(temp)
    direct.append(temp_dir)

def draw_arrow(X, Y, way):
    long = 0.2
    target = (0, 0) #dx dy
    if (way == 0): # down
        target = (0, -long)
    elif (way == 1): # up
        target = (0, long)
    elif (way == 2): # left
        target = (-long, 0)
    elif (way == 3): # right
        target = (long, 0)
    plt.arrow(X+0.5, Y+0.5, target[0], target[1], width=0.03, head_width =0.15)

data = np.array(data)
direct = np.array(direct)
# print(data)
# print(direct)
sns.heatmap(data=data, cmap=cmap)
plt.xlabel('x')
plt.ylim(0, 30)
plt.xlim(0, 30)
plt.ylabel('y')
for i in range(len(direct)):
    for j in range(len(direct[0])):
        draw_arrow(j, i, direct[i][j])

plt.show()
