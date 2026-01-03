import numpy as np

class OrthogonalRotation:
    def __init__(self, dim):
        Q, _ = np.linalg.qr(np.random.randn(dim, dim))
        self.R = Q

    def step(self, X, t):
        return X @ ((1 - t) * np.eye(X.shape[1]) + t * self.R)


class LinearInterpolation:
    def __init__(self, dim):
        self.A = np.eye(dim)
        self.B = np.random.randn(dim, dim)

    def step(self, X, t):
        return X @ ((1 - t) * self.A + t * self.B)


class LinearInterpNormalized:
    def __init__(self, dim):
        self.A = np.eye(dim)
        self.B = np.random.randn(dim, dim)

    def step(self, X, t):
        Y = X @ ((1 - t) * self.A + t * self.B)
        norms = np.linalg.norm(Y, axis=1, keepdims=True) + 1e-8
        return Y / norms


