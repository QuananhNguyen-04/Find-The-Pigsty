import numpy as np
import random
import tensorflow as tf
import keras
import os

## nothing, up, left, right, crash, target

def predict(x_pos, y_pos, x_dis, y_dis, turns, counting, special="nothing"):
    REWARD = {'0': 0, '1': 1, '2': -0.5, '3': -0.5, 'crashed': -200, 'landed': 100, 'closer': 15, 'further': 1, 'nothing':0}
    
    # HYPER-PARAMETERS FOR LEARNING PROCESS

    EPSILON = 0.1 if turns < 30 else 0.4 # SET FOR EPS-GREEDY ALGO
    GAMMA = 1.0 #discount factor 
    ALPHA = 0.3 #learning rates
    
    model = tf.keras.models.load_model("./rein.keras")
    
    input_tensor = tf.convert_to_tensor(np.array([[x_dis, y_dis]], dtype='float32'))
    Q = np.array(model.call(input_tensor))
    Q = np.reshape(Q, (-1))
    Q_next = np.ones(shape=4, dtype='float16')
    this_reward = np.zeros(shape=4, dtype='float16')

    target_x, target_y = x_pos - x_dis, y_pos + y_dis
    pre_dis = pow(pow(x_dis, 2) + pow(y_dis, 2), 1/2)

    for action in range(4):
        x_later, y_later = x_pos, y_pos
        y_later += 7
        if action == 2:
            x_later -= 15
        elif action == 3:
            x_later += 15
        elif action == 1:
            y_later -= 25

        input_tensor = tf.convert_to_tensor(np.array([[x_later - target_x, target_y - y_later]], dtype='float32'))
        outputY = np.array(model.call(input_tensor))
        outputY = np.reshape(outputY, (-1))
        Q_next[action] = np.max(outputY)

        x_later -= target_x
        y_later = target_y - y_later
        dis = pow(pow(x_later, 2) + pow(y_later, 2), 1/2)
        this_reward[action] += REWARD[str(action)]
        this_reward[action] += REWARD[special]+ (REWARD['closer'] if pre_dis > dis else REWARD['further'])
    
    Q = Q + ALPHA * (this_reward + GAMMA * Q_next - Q)
    
    explore_rate = random.random()
    if (explore_rate < EPSILON):
        predictions = random.randint(0, 3)
    else:
        predictions = np.argmax(Q)
    
    counting[predictions] += 1
    actions = np.zeros(shape=4, dtype="int")
    actions[predictions] = 1

    print(f"{x_pos},{y_pos},{x_dis},{y_dis},", end="")
    print(*actions, sep=",",end="," )
    print(f"{x_later},{y_later},",end="")
    print(Q[predictions], end="\n")
    return counting, predictions

# use for initialize Q_next in gen1, 2
def compute_reward(x_pos, y_pos, x_dis, y_dis, action ,x_later, y_later, special='nothing'):
    REWARD = {'0': 0, '1': 1, '2': -0.5, '3': -0.5, 'crashed': -100, 'landed': 100, 'closer': 10, 'further': -10, 'nothing':0}
    GAMMA = 0.8
    pre_dis = pow(pow(x_dis, 2) + pow(y_dis, 2), 1/2)
    dis = pow(pow(x_later, 2) + pow(y_later, 2), 1/2)
    this_reward = REWARD[str(action)] + REWARD[special]+ (REWARD['closer'] if pre_dis > dis else REWARD['further'])

    Q = this_reward + GAMMA * random.randint(-10, 15)
    actions = np.zeros(shape=4, dtype="int")
    actions[action] = 1
    print(f"{x_pos},{y_pos},{x_dis},{y_dis},", end="")
    print(*actions, sep=",",end="," )
    print(f"{x_later},{y_later},",end="")
    print(Q)
