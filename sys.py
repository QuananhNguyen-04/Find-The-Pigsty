import os
import random

fileO = open("state.data", 'w')


for i in range(3):
    file = open(f"state{i}.data", 'r')
    data = file.readlines()[2:]
    fileO.writelines(data)
    file.close()
    data = []

fileO.close()