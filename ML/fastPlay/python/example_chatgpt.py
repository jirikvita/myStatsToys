#!/usr/bin/python
# 24.9.2024
# Q: can you please generate python code that reads N float inputs, trains a fully connected neural network for 2 output float number nodes?

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

# Function to generate the dataset (replace this with actual input data)
def generate_dataset(num_samples, input_size):
    # Random float inputs and two float outputs
    X = np.random.rand(num_samples, input_size)
    Y = np.random.rand(num_samples, 2)  # 2 output float numbers
    return X, Y

# Parameters
N = 10  # Number of input features (change based on your requirement)
num_samples = 1000  # Number of samples in the dataset
epochs = 50  # Number of epochs for training

# Generate the dataset
X, Y = generate_dataset(num_samples, N)

# Build the model
model = Sequential()
model.add(Dense(64, input_dim=N, activation='relu'))  # Input layer and first hidden layer
model.add(Dense(32, activation='relu'))  # Second hidden layer
model.add(Dense(2, activation='linear'))  # Output layer (2 outputs, no activation for regression)

# Compile the model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Train the model
model.fit(X, Y, epochs=epochs, batch_size=32, validation_split=0.2)

# Predict for a new random input
new_input = np.random.rand(1, N)
predicted_output = model.predict(new_input)

print(f"Predicted output: {predicted_output}")
