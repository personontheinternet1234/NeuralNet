import nodes
import numpy as np
from matplotlib import pyplot as plt

actualDataSet = [
    [0,0],
    [0.5,1],
    [1,0]
]

def relU(x):  # Rectified linear activation function
    return max(0,x)

# graph
mygraph = nodes.Graph("mygraph")

# Nodes
input_node = nodes.Node("input")

top_relu = nodes.Node("top_relu", bias=0)

bottom_relu = nodes.Node("bottom_relu", bias=0)

output_node = nodes.Node("output", bias=0)

# connections
input_node.new_connection(input_node, top_relu, weight=round(np.random.normal(loc = 0.0, scale = 1.0, size = None), 4))
input_node.new_connection(input_node, bottom_relu, weight=round(np.random.normal(loc = 0.0, scale = 1.0, size = None), 4))

top_relu.new_connection(top_relu, output_node, weight=round(np.random.normal(loc = 0.0, scale = 1.0, size = None), 4))

bottom_relu.new_connection(bottom_relu, output_node, weight=round(np.random.normal(loc = 0.0, scale = 1.0, size = None), 4))

#adding to graph
mygraph.add_node(input_node)
mygraph.add_node(top_relu)
mygraph.add_node(bottom_relu)
mygraph.add_node(output_node)

def forward(input):
    input_node.activationEnergy = input

    top_relu.activationEnergy = relU(input_node.activationEnergy * input_node.connections[0].weight + top_relu.bias)
    bottom_relu.activationEnergy = relU(input_node.activationEnergy * input_node.connections[1].weight + bottom_relu.bias)

    output_node.activationEnergy = (top_relu.activationEnergy * top_relu.connections[0].weight) + (bottom_relu.activationEnergy * bottom_relu.connections[0].weight) + output_node.bias

    return round(output_node.activationEnergy, 4)

def SSR(actualDataSet):  # sum of squared values function
    sum = 0
    for point in actualDataSet:
        sum += (forward(point[0]) - point[1]) ** 2 # for each x value
    return sum

def new_value(actualDataSet, oldWeight):  # gradient descent function for a given connection's weight.
    # take derivitive of sum of squared values with respect to w4:
    # sum of each data point: 2 * (observed - predicted) * -1

    sum = 0
    for point in actualDataSet:
        sum += -2 * (forward(point[0]) - point[1])
    print("SSR (should approach 0): " + str(SSR(actualDataSet)))

    # returns next weight or bias the connection should have
    return round(oldWeight - (sum * learningRate), 4)

def convert(dataset):
    data = np.array(dataset)
    return [data[:, 0], data[:, 1]]

# for node in mygraph.nodes:
#     for connection in node.connections:
#         print(connection.return_name() + " weight: " + str(connection.weight), end=" ")
#     print("")
#
# print(f"Nodes in graph: ")
# for node in mygraph.nodes:
#     print(node.name + " Energy: " + str(node.activationEnergy) + " Bias: " + str(node.bias))
#
# print(forward(2))

epochs = 0
learningRate = 0
while epochs <= 0:
    epochs = int(input("How many epochs: "))
while learningRate <= 0:
    learningRate = float(input("Learning Rate: "))

for i in range(epochs):
    output_node.bias = new_value(actualDataSet, output_node.bias)
    print("new bias: " + str(output_node.bias))

plt.plot(convert(actualDataSet)[0], convert(actualDataSet)[1])


x = []
y = []
for i in range(100):
    x.append(i/100)
    y.append(forward(i/100))
plt.plot(x, y)

plt.show()