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


def assert_approx_equal(a, b, rtol=0.001):
    if isinstance(a, np.ndarray):
        assert(np.allclose(a, b))
    elif isinstance(a, float) or isinstance(a, np.float) or isinstance(a, np.float32) or isinstance(a, np.float64):
        if a == 0.0 and b == 0.0:
            return
        assert(abs(a - b) / max(abs(a), abs(b)) < rtol)
    else:
        assert(np.all(a == b))
