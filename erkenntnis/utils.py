import numpy as np


def random_position(scale: float = 1.0):
    return np.array([scale * (2.0 * np.random.rand() - 1.0),
                     scale * (2.0 * np.random.rand() - 1.0),
                     0.0])
