#!/usr/bin/python

# 24.9.2024

# https://stackoverflow.com/questions/75608323/how-do-i-solve-error-externally-managed-environment-every-time-i-use-pip-3

# ChatGPT, modified:

# TODO:
# for events read:
# x,y map
# E, xmax map
# etc

import os, sys

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

def plotBias(predictedY,trueY, **kwargs):
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
        print(f'E:    true: {eTrue:10.1f}    predicted: {ePred:10.1f}')
        print(f'Xmax: true: {xmaxTrue:10.1f} predicted: {xmaxPred:10.1f}')
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

    # Create a figure with 1 row and 2 columns of subplots
    plt.figure(figsize=(9, 9))
    
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
    #plt.tight_layout()
    plt.subplots_adjust(bottom=0.1)
    plt.subplots_adjust(left=0.1)

    plt.subplot(2, 2, 3)
    plt.scatter(eTrues, ePreds, c='red', s=5, alpha = 0.01)
    plt.xlabel('true logE')
    plt.ylabel('predicted logE')
    #plt.title('logE scatter')
    plt.xlim(16, 21)
    plt.ylim(16, 21)
    plt.subplots_adjust(bottom=0.1)
    plt.subplots_adjust(left=0.1)
    #plt.tight_layout()
    corre = np.corrcoef(eTrues, ePreds)
    print(f'E correlation factor: {corre}')
    
    plt.subplot(2, 2, 4)
    plt.scatter(xmaxTrues, xmaxPreds, c='blue', s=5, alpha = 0.01)
    plt.xlabel(r'true $X_{max}$')
    plt.ylabel(r'predicted $X_{max}$')
    #plt.title('X_{max} scatter')
    plt.xlim(150, 1200)
    plt.ylim(150, 1200)
    plt.subplots_adjust(bottom=0.1)
    corrx = np.corrcoef(xmaxTrues, xmaxPreds)
    print(f'Xmax correlation factor: {corrx}')

    #plt.subplots_adjust()
    #plt.tight_layout()

    # Show the plots
    tag = ''
    if 'tag' in kwargs:
        tag = kwargs['tag']
    plt.savefig(f'biases{tag}.png')
    plt.savefig(f'biases{tag}.pdf')
    plt.show()
    
##########################################
def concatData(data):
    vals = []
    for dss in data:
        for ds in dss:
            vals.append(ds)
    return vals

##########################################
def ReadAndParseData(infname, i1, i2, **kwargs):
    Data = readData(infname, i1, i2, **kwargs)
    ys = []
    xs = []
    for data in Data:
        logE = data[0]['logE']
        Xmax = data[0]['Xmax']
        ys.append( [logE, Xmax] )
        # to rething!
        # maybe later extract features from each trace separately
        # and not from concatenated data?
        # or does not matter?
        xxs = concatData(data[1])
        if len(xxs) > 0:
            xs.append(xxs)

    debug = 0
    if 'debug' in kwargs:
        debug = kwargs['debug']
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
def main(argv):

    # central vals and sigma around them to accept
    restrictions = { #'logE' : [ [18, 19, 20], 0.25],
                    #'Xmax' : [ [750], 100],
                     'Azimuth' : [ [0.], 180],
                     'Zenith' : [ [45.], 45],
                     'Corex' : [ [-18000], 7000],
                     'Corey' : [ [-22000], 7000]
                    }

    #infname = '/home/qitek/work/github/myStatsToys/FastProcessing/ascii_5k.txt'
    infname = '/home/qitek/work/github/myStatsToys/FastProcessing/ascii_full.txt'

    i1 = 0
    i2 = -1
    debug = 0
    verb = 10000
    X, Y = ReadAndParseData(infname, i1, i2, debug=debug, verb=verb, skip='odd', restrictions = restrictions)

    """
    Recurrent Neural Networks (RNNs) & LSTMs for Sequential Data
    For time series or textual data, RNNs, Long Short-Term Memory Networks (LSTMs), and Transformers can automatically learn temporal features.
    Once trained, these networks can provide feature representations from their hidden states or intermediate layers.
    """

    n_events = len(X)  # Number of samples in the dataset
    input_dim = len(X[0])      # Number of original input features

    print(f'Read events       : {len(X)}')
    print(f'Original features : {input_dim}')

    # desired features:
    Nfeat = 64
    print(f'Desired transformed features : {Nfeat}')

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

    #####################
    # Build the model
    
    model = Sequential()

    # activations: relu, sigmoid, linear
    # kernel_initializer=RandomNormal(mean=0.0, stddev=0.05), bias_initializer='zeros'
    #, input_shape=(32,)),

    N1, N2, N3, N4 = 256, 128, 64, 32
    model.add(Dense(N1, input_dim=Nfeat, activation='relu'))  # Input layer and first hidden layer
    model.add(BatchNormalization())                           # batch normalization of the output
    if N2 > 0:
        model.add(Dense(N2, activation='relu'))               # Second hidden layer
    if N3 > 0:
        model.add(Dense(N3, activation='relu'))               # Third hidden layer
    if N4 > 0:
        model.add(Dense(N3, activation='relu'))               # Fourth hidden layer
    model.add(Dense(2, activation='linear'))                  # Output layer (2 outputs, no activation for regression)

    #####################
    # Compile the model
    # other examples:
    # loss='binary_crossentropy', metrics=['accuracy']
    # other optimizers: SGD, default learning rate 0.01
    # Adam: 0.0001


    #####################
    # Training parameters
    learning_rate = 0.0002 # learning rate
    epochs = 100           # Number of epochs for training
    batch_size = 50        # batch size
        
    optimizer = Adam(learning_rate=learning_rate)  # Change learning rate here
    #optimizer = SGD(learning_rate=0.01)  # Change learning rate here

    print('Model summary:')
    model.summary()
    total_params = model.count_params()
    print(f"Total number of parameters: {total_params}")

    model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])

    #####################
    # Train the model
    model.fit(features, Y, epochs=epochs, batch_size=batch_size, validation_split=0.2)
    print('Done training!')
    #print('Printing the model...')
    #printWeights(model)
    
    print('Going to test the trained model...')
    slearning_rate = str(learning_rate).replace('.','p')
    mtag = f'_LSTM_i1_{i1}_i2_{i2}_epochs_{epochs}_lrate_{slearning_rate}_Nfeat_{Nfeat}_Neurons_{N1}_{N2}_{N3}_{N4}'

    ##########################################
    # Plot performance on the train datase:
    train_predictedY = model.predict(features)
    plotBias(train_predictedY, Y, tag = mtag + '_train')
    
    ##########################################
    # Predict for a new input
    #i3 = i2 + 10000
    print('Reading test events...')
    testX, trueY = ReadAndParseData(infname, i1, i2, verb = 10000, debug=0, skip='even', restrictions = {})
    print(f'Read test events  : {len(testX)}')
    
    testX_reshaped = np.expand_dims(testX, axis=1)
    testfeatures = feature_extractor.predict(testX_reshaped)

    predictedY = model.predict(testfeatures)
    print(f"Predicted output: {predictedY}")

    # save
    #print('Saving the model...')
    #model.save(f'model_{mtag}.keras')

    # load in usage:
    # from tensorflow.keras.models import load_model
    # Load the model
    # model = load_model('model.keras')

    plotBias(predictedY, trueY, tag = mtag + '_test')


###################################
###################################
###################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
###################################
###################################
###################################
