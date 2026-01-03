import numpy as np

def make_ring(n=400, dim=10, noise=0.05):
    angles = np.random.rand(n) * 2 * np.pi
    X = np.zeros((n, dim))
    X[:, 0] = np.cos(angles)
    X[:, 1] = np.sin(angles)
    X += noise * np.random.randn(n, dim)
    return X
