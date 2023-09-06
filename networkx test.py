import networkx as nx
import matplotlib.pyplot as plt

import nodes
import numpy as np
import math
from matplotlib import pyplot as plt

"""
This program uses the nodes structure to practice basic backpropagation.
Made from scratch (No tutorials, no pytorch).
Version: 0.1
Author: Isaac Park Verbrugge
"""

actualDataSet = [
    [0,0],
    [0.5,1],
    [1,0]
]

# Connection = edge

def softplus(x):  # SoftPlus activation function
    return math.log(1 + math.e**x)

def softmax(outputNodes):
    denom = 0
    for i in outputNodes:
        denom += math.e ** outputNodes[i].activationEnergy

    softOutputEnergies = []
    for i in outputNodes:
        softOutputEnergies.append((math.e**outputNodes[i].activationEnergy)/denom)

    return softOutputEnergies

def softmax_derivative():
    # TODO
    ...


G = nx.Graph()
def create_graph(graph, number_input_nodes, number_hidden_layers, number_nodes_per_layer, number_output_nodes):

    # layer matrix sizing
    for iterator in range(number_hidden_layers):
        graph.layers.append([])

    # input node creation
    for i in range(number_input_nodes):
        graph.layers[0].append(nodes.Node(i, graph, 0, energy=0, bias=0))
        G.add_node(i, pos=(0, i))

    # hidden node creation
    for l in range(number_hidden_layers):
        current_layer = l + 1
        for n in range(number_nodes_per_layer):
            graph.layers[current_layer].append(nodes.Node(i + n + 1, graph, current_layer, energy=0, bias=0))
            G.add_node(i + n + 1, pos=(current_layer, n))

    # output node creation
    for o in range(number_output_nodes):
        last_layer = len(graph.layers) - 1
        graph.layers[last_layer].append(nodes.Node(i + n + 2 + o, graph, last_layer, energy=0, bias=0))
        G.add_node(i + n + 2 + o, pos=(last_layer, o))

    # connections
    for i in range(len(graph.layers) - 1):

        # print("try#: " + str(i) + str(graph.layers[i]))
        # print(graph.layers[i + 1])

        for originnode in graph.layers[i]:
            for destinationnode in graph.layers[i + 1]:
                originnode.new_connection(originnode, destinationnode, np.random.normal(0, 5))
                G.add_edge(int(originnode.name),int(destinationnode.name))

    # np stuff for np.matmult()
    for i in range(len(graph.layers)):
        graph.layers[i] = np.array(graph.layers[i])

def backward():
    # usage: node1-2 = add_backprop(node1-2.upstreamValue())
    def multiply_backprop(upstream_gradient, downstream_nodes, target_node):
        product = upstream_gradient
        for node in downstream_nodes:
            product *= node.activationEnergy
        product /= target_node.activationEnergy

        return product
    def max_backprop(upstream_gradient, downstream_nodes, target_node):
        largest = downstream_nodes[0].activationEnergy
        for node in downstream_nodes:
            if node.activationEnergy >= largest:
                largest = node.activationEnergy

        if target_node.activationEnergy == largest:
            return upstream_gradient
        else:
            return 0
    def copy_backprop(upstream_gradients):  # upstream_gradients is a list tho... Idk where imma use copy_backprop
        sum = 0
        for i in upstream_gradients:
            sum += i
        return sum
    def add_backprop(upstream_gradient):
        return(upstream_gradient)


def SSR(actualDataSet):  # sum of squared values function
    sum = 0
    for point in actualDataSet:
        ...
        #sum += (forward(point[0]) - point[1]) ** 2 # for each x value
    return sum


def new_value(actualDataSet, oldWeight):  # gradient descent function for a given connection's weight.
    # take derivitive of sum of squared values with respect to w4:
    # sum of each data point: 2 * (observed - predicted) * -1

    sum = 0
    for point in actualDataSet:
        ...
        #sum += -2 * (point[1] - forward(point[0]))
    print("SSR (should approach 0): " + str(SSR(actualDataSet)))

    # returns next weight or bias the connection should have
    #return round(oldWeight - (sum * learningRate), 4)

# Just to convert my weird usage of actualDataSet being a matrix.
def convert(dataset):
    data = np.array(dataset)
    return [data[:, 0], data[:, 1]]

mygraph = nodes.Graph("mygraph")
create_graph(mygraph, 1, 1, 2, 2)

# print(mygraph.layers)
for layer in range(len(mygraph.layers)):
    for node in mygraph.layers[layer]:
        for connection in node.connections:
            print("layer" + str(layer) + " " + str(connection.origin.name) + " layer" +
                  str(connection.destination.layer) + " " + str(connection.destination.name))


pos=nx.get_node_attributes(G,'pos')
nx.draw(G, pos, with_labels=True)

plt.show()