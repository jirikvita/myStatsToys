#!/usr/bin/python

# 24.9.2024

# https://stackoverflow.com/questions/75608323/how-do-i-solve-error-externally-managed-environment-every-time-i-use-pip-3

# ChatGPT, modified:

# TODO:
# for events read:
# x,y map
# E, xmax map
# etc

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization
import numpy as np
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.initializers import RandomNormal, HeNormal


from tensorflow.keras.layers import LSTM, Embedding, Input
from tensorflow.keras.models import Model

import matplotlib.pyplot as plt

from readData import *


##########################################
def printWeights(model):
    for layer in model.layers:
        weights = layer.get_weights()  # Returns a list of weights (and biases)
        print(f"Layer {layer.name}:")
        
        # Check if the layer has weights
        if weights:
            print("Weights:", weights[0].shape)  # Print weights shape
            if len(weights) > 1:  # Some layers may not have biases
                print("Biases:", weights[1].shape)  # Print biases shape
        else:
            print("No weights for this layer.")
            """
            # Print all trainable weights
for layer in model.layers:
    print(f"Layer {layer.name} trainable weights:")
    for weight in layer.trainable_weights:
        print(weight.name, weight.shape)

# Print all non-trainable weights
for layer in model.layers:
    print(f"Layer {layer.name} non-trainable weights:")
    for weight in layer.non_trainable_weights:
        print(weight.name, weight.shape)

        """

##########################################

def plotBias(eBias, xmaxBias, eTrues, ePreds, xmaxTrues, xmaxPreds):
    # Create a figure with 1 row and 2 columns of subplots
    plt.figure(figsize=(10, 10))
    
    # First subplot (left)
    plt.subplot(2, 2, 1)  # 1 row, 2 columns, 1st subplot
    plt.hist(eBias, bins=25, color='red', alpha=0.7)
    #plt.title('logE bias')
    plt.xlabel(r'logE: (predicted-true)/true')
    
    # Second subplot (right)
    plt.subplot(2, 2, 2)  # 1 row, 2 columns, 2nd subplot
    plt.hist(xmaxBias, bins=25, color='blue', alpha=0.7)
    #plt.title('Xmax bias')
    plt.xlabel(r'$X_{max}$: (predicted-true)/true')
    
    # Adjust the layout to prevent overlap
    plt.tight_layout()

    plt.subplot(2, 2, 3)
    plt.scatter(eTrues, ePreds, c='red', s=15, alpha = 0.7)
    plt.xlabel('true logE')
    plt.ylabel('predicted logE')
    #plt.title('logE scatter')
    #plt.xlim(15, 20)
    #plt.ylim(15, 20)

    plt.subplot(2, 2, 4)
    plt.scatter(xmaxTrues, xmaxPreds, c='blue', s=15, alpha = 0.7)
    plt.xlabel(r'true $X_{max}$')
    plt.ylabel(r'predicted $X_{max}$')
    #plt.title('X_{max} scatter')
    #plt.xlim(150, 1000)
    #plt.ylim(150, 1000)


    plt.subplots_adjust()
    # Show the plots
    plt.show()
    plt.savefig('biases.png')
    
##########################################

def concatData(data):
    vals = []
    for dss in data:
        for ds in dss:
            vals.append(ds)
    return vals

##########################################
def ReadAndParseData(infname, i1, i2, debug, restrictions):
    Data = readData(infname, i1, i2, restrictions, 0, 10000)
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

# central vals and sigma around them to accept
restrictions = { #'logE' : [ [18, 19, 20], 0.25],
                 'Xmax' : [ [750], 100],
                 'Azimuth' : [ [130], 30],
                 'Zenith' : [ [80], 30],
                 'Corex' : [ [-18000], 5000],
                 'Corey' : [ [-12000], 5000]
                }

#infname = '/home/qitek/work/github/myStatsToys/FastProcessing/ascii_5k.txt'
infname = '/home/qitek/work/github/myStatsToys/FastProcessing/ascii_full.txt'

i1 = 0
i2 = 300000
debug = 0
X, Y = ReadAndParseData(infname, i1, i2, debug, {}) #restrictions)



"""
Recurrent Neural Networks (RNNs) & LSTMs for Sequential Data
For time series or textual data, RNNs, Long Short-Term Memory Networks (LSTMs), and Transformers can automatically learn temporal features.
Once trained, these networks can provide feature representations from their hidden states or intermediate layers.
"""

n_events = len(X)  # Number of samples in the dataset
input_dim = len(X[0])      # Number of original input features
epochs = 100          # Number of epochs for training
print(f'Read events       : {len(X)}')
print(f'Original features : {input_dim}')

# desired features:
Nfeat = 128

print(f'Read events       : {len(X)}')
print(f'Original features : {input_dim}')

X_reshaped = np.expand_dims(X, axis=1)

# Step 2: Define the LSTM Feature Extractor
input_layer = Input(shape=(1, input_dim))  # Correct shape for LSTM input

# Define the LSTM layer with feature extraction (last timestep output)
lstm_out = LSTM(Nfeat, return_sequences=False)(input_layer)  # Nfeat-dimensional output

# Create the feature extractor model
feature_extractor = Model(inputs=input_layer, outputs=lstm_out)

# Step 3: Extract features from the input data
features = feature_extractor.predict(X_reshaped)  # Shape will be (num_samples, Nfeat)
print("Extracted features shape:", features.shape)


"""
# other options:

from sklearn.decomposition import PCA

# Apply PCA for feature extraction
pca = PCA(n_components=10)
reduced_features = pca.fit_transform(input_data)

from tensorflow.keras.layers import GlobalAveragePooling2D

# Add global average pooling layer
x = GlobalAveragePooling2D()(feature_maps)

"""

# Build the model
model = Sequential()

# activations: relu, sigmoid, linear
#kernel_initializer=RandomNormal(mean=0.0, stddev=0.05), bias_initializer='zeros'
#, input_shape=(32,)),

model.add(Dense(256, input_dim=Nfeat, activation='relu'))  # Input layer and first hidden layer
model.add(BatchNormalization())
model.add(Dense(2*128, activation='relu'))               # Second hidden layer
model.add(Dense(64, activation='relu'))                # Third hidden layer
model.add(Dense(2, activation='linear'))               # Output layer (2 outputs, no activation for regression)

#####################
# Compile the model
# other examples:
# loss='binary_crossentropy', metrics=['accuracy']
# other optimizers: SGD, default learning rate 0.01
# Adam: 0.0001

optimizer = Adam(learning_rate=0.0002)  # Change learning rate here
#optimizer = SGD(learning_rate=0.01)  # Change learning rate here

model.summary()
total_params = model.count_params()
print(f"Total number of parameters: {total_params}")

model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])

#####################
# Train the model
model.fit(features, Y, epochs=epochs, batch_size=50, validation_split=0.2)

printWeights(model)

#####################
# Predict for a new input
i3 = i2 + 10000
testX, trueY = ReadAndParseData(infname, i2, i3, 0, {})#, restrictions)

testX_reshaped = np.expand_dims(testX, axis=1)
testfeatures = feature_extractor.predict(testX_reshaped)

predictedY = model.predict(testfeatures)
print(f"Predicted output: {predictedY}")

# save and load
# model.save('model.h5')
# from tensorflow.keras.models import load_model
# Load the model
# model = load_model('model.h5')

eBias = []
xmaxBias = []
ePreds = []
eTrues = []
xmaxPreds = []
xmaxTrues = []
for y,ytrue in zip(predictedY,trueY):
    ePred,xmaxPred = y[0], y[1]
    eTrue,xmaxTrue = ytrue[0], ytrue[1]
    #print('-------------------------------------------')
    #print(f'E:    true: {eTrue:10.1f}    predicted: {ePred:10.1f}')
    #print(f'Xmax: true: {xmaxTrue:10.1f} predicted: {xmaxPred:10.1f}')
    de = ePred - eTrue
    dxmax = xmaxPred - xmaxTrue
    #eBias.append(de)
    #xmaxBias.append(dxmax)
    eBias.append(de / eTrue)
    xmaxBias.append(dxmax / xmaxTrue)

    ePreds.append(ePred)
    eTrues.append(eTrue)
    xmaxPreds.append(xmaxPred)
    xmaxTrues.append(xmaxTrue)


plotBias(eBias, xmaxBias, eTrues, ePreds, xmaxTrues, xmaxPreds)

