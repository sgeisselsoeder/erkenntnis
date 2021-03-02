import numpy as np


def random_position(scale: float = 1.0):
    return np.array([scale * (2.0 * np.random.rand() - 1.0),
                     scale * (2.0 * np.random.rand() - 1.0),
                     0.0])


def normalize_vector_3d(v: np.array):
    # length = np.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    length = np.sqrt(v[0] * v[0] + v[1] * v[1])
    if length == 0.0:
        return v
    return v / length


def vector_length(v: np.array):
    length = np.sqrt(v[0] * v[0] + v[1] * v[1])
    return length
    # return np.linalg.norm(v)
