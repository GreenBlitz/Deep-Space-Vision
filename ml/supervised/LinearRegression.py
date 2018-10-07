import numpy as np
from ml.supervised.PolynomialLearner import Polynomial, linear

def find_polynomial(dim, deg, inp, label):
    poly = Polynomial(dim=dim, deg=deg, func=linear)
    # TODO complete this function

