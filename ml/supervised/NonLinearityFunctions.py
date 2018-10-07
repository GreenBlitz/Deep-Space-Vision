import numpy as np


def sigmoid(x, d=False):
    if d:
        return x*(1-x)
    return 1/(1+np.exp(-x))


def tanh(x, d=False):
    if d:
        return 1-x*x
    return np.tanh(x)


def relu(x, d=False):
    e = np.exp(x)
    if d:
        return (e-1)/e
    return np.log(e+1)


def linear_relu(x, d=False):
    if d:
        return 1 if x > 0 else 0
    elif x > 0:
        return x
    return 0


linear_relu = np.vectorize(linear_relu)


def create_parametric_relu(a):
    def parametric_relu(x, d=False):
        if d:
            return 1 if x > 0 else a
        return x if x > 0 else a*x
    return np.vectorize(parametric_relu)


def linear(x, d=False):
    return 1 if d else x


linear = np.vectorize(linear)


def arctan(x, d=False):
    if d:
        return 1/(1+np.tan(x)**2)
    return np.arctan(x)


def softmax(x, d=False):
    if d:
        return x*(1-x)
    e = np.exp(x)
    return e/(1+e)

