import numpy as np
import random

# Generate a random scalar
# random_scalar = int(11 * np.random.rand())
# training_choice = random.randint(0, 10)
# rs = tc = 0
# for i in range(1000000):
#     rs += int(11 * np.random.rand())
#     tc += random.randint(0, 10)
# print(rs / 1000000)
# print(tc / 1000000)

list1 = [
    [0.4,1.5,200,0.1]
]

list1[0] = np.minimum(1, list1[0])
print(list1[0])