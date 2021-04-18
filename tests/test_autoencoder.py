import numpy as np
from erkenntnis.brain_implementation.ai.autoencoder import Autoencoder


def average_error_examples(ae, data, number_pixels, number_examples=10):
    average_error_test_set = 0.0
    for i in range(number_examples):
        next_image = np.reshape(data[i], newshape=(1, number_pixels))
        result = ae.predict(next_image)
        average_error = np.sum(np.abs(result - next_image)) / number_pixels
        average_error_test_set += average_error

    return average_error_test_set


def test_autoencoder_convergence():
    number_pixels = 10
    data = np.zeros(shape=(1024, number_pixels), dtype=np.float32)
    data[:, 5] = 1.0
    data[::2, 2] = 1.0

    ae = Autoencoder(latent_space_size=3)
    ae.fit(x=data, number_epochs=1)
    average_error_test_set_1 = average_error_examples(ae=ae, data=data, number_pixels=number_pixels)

    ae.fit(x=data, number_epochs=30)
    average_error_test_set_2 = average_error_examples(ae=ae, data=data, number_pixels=number_pixels)

    assert(average_error_test_set_2 < average_error_test_set_1)


def test_autoencoder_construction():
    ae = Autoencoder(latent_space_size=3)


def test_autoencoder_fit_possible():
    number_pixels = 10
    data = np.zeros(shape=(1024, number_pixels), dtype=np.float32)
    data[:, 5] = 1.0
    data[::2, 2] = 1.0

    ae = Autoencoder(latent_space_size=3)
    ae.fit(x=data, number_epochs=1)
