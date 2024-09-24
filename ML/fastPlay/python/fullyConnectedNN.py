#!/usr/bin/python

# 24.9.2024

# https://stackoverflow.com/questions/75608323/how-do-i-solve-error-externally-managed-environment-every-time-i-use-pip-3

# ChatGPT, modified:

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

from readData import *

##########################################

# Function to generate the dataset (replace this with actual input data)
#def generate_dataset(num_samples, input_size):
#    # Random float inputs and two float outputs
#    X = np.random.rand(num_samples, input_size)
#    Y = np.random.rand(num_samples, 2)  # 2 output float numbers
#    return X, Y

##########################################

def concatData(data):
    vals = []
    for dss in data:
        for ds in dss:
            vals.append(ds)
    return vals

##########################################
def ReadAndParseData(infname, i1, i2, debug = 0):
    Data = readData(infname, i1, i2)
    ys = []
    xs = []
    for data in Data:
        logE = data[0]['logE']
        Xmax = data[0]['Xmax']
        ys.append( [logE, Xmax] )
        xxs = concatData(data[1])
        if len(xxs) > 0:
            xs.append(xxs)

    if debug:
        print('-----------------------------------------------')
        print(xs)
        print('-----------------------------------------------')
        print(ys)
        print('-----------------------------------------------')
        for x in xs:
            print(len(x))
        print('-----------------------------------------------')
        for y in ys:
            print(len(y))
    
    rows = len(xs)
    cols = len(xs[0])
    X = np.array(xs, dtype=float).reshape(rows, cols)
    rows = len(ys)
    cols = len(ys[0])
    Y = np.array(ys).reshape(rows, cols)
    return X, Y

##########################################

#infname = '/home/qitek/work/github/myStatsToys/FastProcessing/ascii_5k.txt'
infname = '/home/qitek/work/github/myStatsToys/FastProcessing/ascii_full.txt'

i1 = 0
i2 = 1000
X, Y = ReadAndParseData(infname, i1, i2)

# Parameters
N = len(X[0]) # # Number of input features
num_samples = len(X)  # Number of samples in the dataset
epochs = 50  # Number of epochs for training


# Build the model
model = Sequential()
model.add(Dense(64, input_dim=N, activation='relu'))  # Input layer and first hidden layer
model.add(Dense(32, activation='relu'))  # Second hidden layer
model.add(Dense(2, activation='linear'))  # Output layer (2 outputs, no activation for regression)

# Compile the model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Train the model
model.fit(X, Y, epochs=epochs, batch_size=32, validation_split=0.2)

# Predict for a new input
i3 = i2 + 10
testX, trueY = ReadAndParseData(infname, i2, i3)
predictedY = model.predict(testX)
print(f"Predicted output: {predictedY}")

for y,ytrue in zip(predictedY,trueY):
    ePred,xmaxPred = y[0], y[1]
    eTrue,xmaxTrue = ytrue[0], ytrue[1]
    print('-------------------------------------------')
    print(f'E: true: {eTrue} predicted: {ePred}')
    print(f'E: true: {xmaxTrue} predicted: {xmaxPred}')
    
