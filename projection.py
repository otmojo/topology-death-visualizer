import numpy as np

class FixedProjection:
    def __init__(self, dim):
        P = np.random.randn(dim, 2)
        self.P = P / np.linalg.norm(P, axis=0, keepdims=True)

    def project(self, X):
        return X @ self.P
