"""
A Neural Network made using only mathematical functions
Isaac Park Verbrugge & Christian SW Host-Madsen
"""

import ast
import math
import random
import time

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from tqdm import tqdm

""" definitions """


# split training and testing data
def test_train_split(data, test_size):
    random.shuffle(data)
    test = data[0:round(len(data) * test_size)]
    train = data[round(len(data) * test_size):]
    return train, test


# xavier initialization
def xavier_initialize(length, width):
    array = np.random.randn(length, width) * math.sqrt(2 / length)
    return array


# leaky rectified linear activator
def l_relu(values):
    output = np.maximum(0.1 * values, values)
    return output


# derivative of leaky rectified linear activator
def d_l_relu(values):
    output = np.where(values > 0, 1, 0.1)
    return output


# forward pass
def forward(inputs, weights, biases):
    nodes = [inputs]
    for layer in range(layers - 1):
        activations = l_relu(np.matmul(nodes[-1], weights[layer]) + biases[layer])
        nodes.append(activations)
    return nodes


# sgd backpropagation
def sgd_backward(nodes, expected, weights, biases):
    # initialize gradient lists
    d_weights = []
    d_biases = []

    d_b = -2 * (expected - nodes[-1])
    d_biases.insert(0, d_b)
    for layer in range(-1, -len(nodes) + 1, -1):
        d_w = nodes[layer - 1].T * d_b
        d_weights.insert(0, d_w)
        d_b = np.array([np.sum(weights[layer] * d_b, axis=1)])
        d_biases.insert(0, d_b)
    d_w = nodes[0].T * d_b
    d_weights.insert(0, d_w)

    for layer in range(len(nodes) - 1):
        weights[layer] -= learning_rate * (d_weights[layer] + (alpha / train_len) * weights[layer])
        biases[layer] -= learning_rate * d_biases[layer]

    return weights, biases


# tensor backpropagation
def tensor_backward(nodes, expected, weights, biases):
    # initialize gradient lists
    d_weights = []
    d_biases = []

    d_b = -2 * (expected - nodes[-1])
    d_biases.insert(0, d_b)
    for layer in range(-1, -len(nodes) + 1, -1):
        d_w = np.reshape(nodes[layer - 1], (tensor_time, layer_sizes[layer - 1], 1)) * d_b
        d_weights.insert(0, d_w)
        d_b = np.reshape(np.array([np.sum(weights[layer] * d_b, axis=2)]), (tensor_time, 1, layer_sizes[layer - 1]))
        d_biases.insert(0, d_b)
    d_w = np.reshape(nodes[0], (tensor_time, layer_sizes[0], 1)) * d_b
    d_weights.insert(0, d_w)

    for layer in range(len(nodes) - 1):
        weights[layer] -= learning_rate * np.sum((d_weights[layer] + (alpha / tensor_time) * weights[layer]), axis=0) / tensor_time
        biases[layer] -= learning_rate * np.sum(d_biases[layer], axis=0) / tensor_time

    return weights, biases


# graph confusion matrix
def plot_cm(cm, title=None, labels=None, color="Blues"):
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=labels
    )
    disp.plot(cmap=color)
    disp.ax_.set_title(title)
    plt.show()


""" program settings """

# network hyperparameters
# learn = True
# activation = "Leaky ReLU"
# solver = "SGD"
# hidden_layer_sizes = [16, 16]
# max_iter = 10000
# learning_rate = 0.001
# alpha = 0.1
# batch_size = 42
# validation_frac = 0.3

# dataset parameters
# trim_dataset = False
# trim_frac = 0.1
# values_file_path = "data_values_keras.csv"
# labels_file_path = "data_labels_keras.csv"

# output configuration
# graph_results = True
# cm_normalization = "true"
# eval_batching = True
# eval_batch_size = 5
# eval_interval = 10

# model settings
# network_version = "1.5"
# load_trained = False
# save_trained = False
# weights_location = "weights_keras.txt"
# biases_location = "biases_keras.txt"

# network superparams
learn = True
sgd = False
tensor_time = 42
load = False
save = False
layer_sizes = [784, 16, 16, 10]
epochs = 10000
learning_rate = 0.001
alpha = 0.1

# dataset params
test_frac = 0.3
trim = False
trim_value = 4200

# user information
graphs = True
messy_plot = True
messy_plot_time = 5
normalization = "true"
log_rate = 10
nn_version = "1.4"

# file locations
df_values_location = "data_values_keras.csv"
df_labels_location = "data_labels_keras.csv"
weights_location = "weights_keras.txt"
biases_location = "biases_keras.txt"

""" network generation """

print(f"Neural Network From Scratch (Version {nn_version})")

# load dataset
df_values = np.array(pd.read_csv(f"data/{df_values_location}")).tolist()
for i in tqdm(range(len(df_values)), ncols=150, desc="Reformatting Data Values"):
    df_values[i] = np.array([df_values[i]])
df_labels = np.array(pd.read_csv(f"data/{df_labels_location}")).tolist()
for i in tqdm(range(len(df_labels)), ncols=150, desc="Reformatting Data Labels"):
    df_labels[i] = np.array([df_labels[i]])

# split training and testing data
train, test = test_train_split(list(zip(df_values, df_labels)), test_size=test_frac)
# unzip training and testing data
X, Y = zip(*train)
X_test, Y_test = zip(*test)
# trim dataset
if trim:
    X, Y = list(X)[0:trim_value], list(Y)[0:trim_value]
else:
    X, Y = list(X), list(Y)
# reformat training and testing data
X_test, Y_test = list(X_test), list(Y_test)
array_X, array_Y = np.array(X), np.array(Y)
array_X_test, array_Y_test = np.array(X_test), np.array(Y_test)

# network values
layers = len(layer_sizes)
train_len = len(X)
test_len = len(X_test)

# instantiate weights and biases
weights = []
biases = []
if load:
    # load weights and biases
    with open(f"saved/{weights_location}", "r") as f:
        for line in f:
            weights.append(np.array(ast.literal_eval(line)))
    with open(f"saved/{biases_location}", "r") as f:
        for line in f:
            biases.append(np.array(ast.literal_eval(line)))
else:
    # generate weights and biases
    for i in range(layers - 1):
        weights.append(xavier_initialize(layer_sizes[i], layer_sizes[i + 1]))
        biases.append(np.zeros((1, layer_sizes[i + 1])))

""" network training """

start_time = time.time()

logged_losses = []
logged_losses_test = []
if learn:
    # training loop
    for epoch in tqdm(range(epochs), ncols=150, desc="Training"):
        if sgd:
            # SGD
            # test choice
            tc = random.randint(0, train_len - 1)
            inputs = X[tc]
            expected = Y[tc]

            # forward pass
            nodes = forward(inputs, weights, biases)

            # backpropagation
            weights, biases = sgd_backward(nodes, expected, weights, biases)

            # loss calculation
            if epoch % log_rate == 0:
                # SSR
                if messy_plot:
                    tc_test = random.randint(0, test_len - 1)
                    train_predicted = nodes[-1]
                    test_predicted = forward(X_test[tc_test], weights, biases)[-1]
                    loss = np.sum(np.subtract(expected, train_predicted) ** 2)
                    test_loss = np.sum(np.subtract(Y_test[tc_test], test_predicted) ** 2)
                else:
                    train_predicted = forward(array_X, weights, biases)[-1]
                    test_predicted = forward(array_X_test, weights, biases)[-1]
                    loss = np.sum(np.subtract(array_Y, train_predicted) ** 2) / train_len
                    test_loss = np.sum(np.subtract(array_Y_test, test_predicted) ** 2) / test_len
                logged_losses.append(loss)
                logged_losses_test.append(test_loss)
        else:
            # tensors
            # data selection
            tc = random.randint(tensor_time, train_len)
            inputs = array_X[tc - tensor_time:tc]
            expected = array_Y[tc - tensor_time:tc]

            # forward pass
            nodes = forward(inputs, weights, biases)

            # backpropagation
            weights, biases = tensor_backward(nodes, expected, weights, biases)

            # loss calculation
            if epoch % log_rate == 0:
                # SSR
                if messy_plot:
                    tc_test = random.randint(tensor_time, test_len)
                    train_predicted = nodes[-1]
                    test_predicted = forward(array_X_test[math.floor(tc_test - tensor_time * test_frac):tc_test], weights, biases)[-1]
                    loss = np.sum(np.subtract(expected, train_predicted) ** 2) / tensor_time
                    test_loss = np.sum(np.subtract(array_Y_test[math.floor(tc_test - tensor_time * test_frac):tc_test], test_predicted) ** 2) / math.ceil(tensor_time * test_frac)
                else:
                    train_predicted = forward(array_X, weights, biases)[-1]
                    test_predicted = forward(array_X_test, weights, biases)[-1]
                    loss = np.sum(np.subtract(array_Y, train_predicted) ** 2) / train_len
                    test_loss = np.sum(np.subtract(array_Y_test, test_predicted) ** 2) / test_len
                logged_losses.append(loss)
                logged_losses_test.append(test_loss)

end_time = time.time()

""" data saving """

# save optimized weights and biases
if save:
    with open(f"saved/{weights_location}", "w") as f:
        for array in tqdm(range(len(weights)), ncols=150, desc="Saving Weights"):
            f.write(str(weights[array].tolist()) + "\n")
    with open(f"saved/{biases_location}", "w") as f:
        for array in tqdm(range(len(biases)), ncols=150, desc="Saving Biases"):
            f.write(str(biases[array].tolist()) + "\n")

""" result calculation """

# train loss
train_predicted = forward(X, weights, biases)[-1]
loss = np.sum(np.subtract(Y, train_predicted) ** 2) / train_len
# test loss
test_predicted = forward(X_test, weights, biases)[-1]
loss_test = np.sum(np.subtract(Y_test, test_predicted) ** 2) / test_len

# train accu
accu = 0
for i in tqdm(range(len(X)), ncols=150, desc="Calculating Training Accuracy"):
    predicted = forward(X[i], weights, biases)[-1]
    expected = Y[i]
    if np.nanargmax(predicted) == np.nanargmax(expected):
        accu += 1
accu /= train_len

# test accu
accu_test = 0
for i in tqdm(range(len(X_test)), ncols=150, desc="Calculating Testing Accuracy"):
    predicted = forward(X_test[i], weights, biases)[-1]
    expected = Y_test[i]
    if np.nanargmax(predicted) == np.nanargmax(expected):
        accu_test += 1
accu_test /= test_len

# matplotlib graphs
if graphs:
    # generate cms
    # train
    y_true = []
    y_pred = []
    for i in tqdm(range(len(X)), ncols=150, desc="Generating Training Confusion Matrix"):
        predicted = forward(X[i], weights, biases)[-1]
        expected = Y[i]
        y_true.append(np.nanargmax(predicted))
        y_pred.append(np.nanargmax(expected))
    cm_train = confusion_matrix(y_true, y_pred, normalize=normalization)

    # test
    y_true_test = []
    y_pred_test = []
    for i in tqdm(range(len(X_test)), ncols=150, desc="Generating Testing Confusion Matrix"):
        predicted = forward(X_test[i], weights, biases)[-1]
        expected = Y_test[i]
        y_true_test.append(np.nanargmax(predicted))
        y_pred_test.append(np.nanargmax(expected))
    cm_test = confusion_matrix(y_true_test, y_pred_test, normalize=normalization)

""" result display """

# print results
print(f"Results - Train Loss: {round(loss, 5)} - Test Loss: {round(loss_test, 5)} - Train Accuracy: {round(accu, 5)} - Test Accuracy: {round(accu_test, 5)} - Elapsed Time: {round(end_time - start_time, 5)}s")

# show matplotlib graphs
if graphs:
    # find label names
    label_names = pd.read_csv(f"data/{df_labels_location}", nrows=0).columns.tolist()
    # graph cms
    plot_cm(cm_train, title="Train Results", labels=label_names)
    plot_cm(cm_test, title="Test Results", labels=label_names)

    # graph loss vs epoch
    plt.plot(range(0, epochs, log_rate), logged_losses, color="blue", alpha=0.5, label="Train")
    plt.plot(range(0, epochs, log_rate), logged_losses_test, color="red", alpha=0.5, label="Test")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Loss v.s. Epoch")
    plt.legend(loc="lower right")
    plt.show()
