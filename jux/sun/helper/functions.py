import numpy as np

"""Helper functions to fit on the detected flares"""

def linear_func(x, m, c):
    return (m*x + c)

def log_exp_func(x, ln_a, b):
    t = -1 * b * np.sqrt(x)
    return (ln_a + t)

def exp_func(x, a, b):
    t = -1 * b * np.sqrt(x)
    y = np.exp(t)
    return (a * y)