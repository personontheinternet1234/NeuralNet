import time

from gardenpy.utils import (
    Initializers,
    Activators,
    Losses,
    Optimizers
)

# algorithm settings
initializer = Initializers('xavier')
activator = Activators('softmax')
loss = Losses('centropy')
optimizer = Optimizers('adam')

time.sleep(0.1)

# initialize values
thetas_in = initializer.initialize(5, 5)
y = initializer.initialize(5, 5)

# forward pass (kind of)
yhat = activator.activate(thetas_in)

# loss and gradient of loss
cost = loss.loss(y, yhat)
d_cost = loss.d_loss(y, yhat)

# gradient of values
d_yhat = activator.d_activate(d_cost)
thetas_out = optimizer.optimize(thetas_in, d_yhat)

# print values
print('thetas_in')
print(thetas_in)
print('----------')
print('y')
print(y)
print('----------')
print('yhat')
print(yhat)
print('----------')
print('cost')
print(cost)
print(type(cost))
print('----------')
print('d_cost')
print(d_cost)
print('----------')
print('d_yhat')
print(d_yhat)
print('----------')
print('thetas_out')
print(thetas_out)
