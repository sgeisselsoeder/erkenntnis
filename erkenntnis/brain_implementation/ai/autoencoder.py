import numpy as np
import pandas as pd
from pathlib import Path
from typing import Union, List

from tensorflow import keras
from .helper.pickle import save_pickle, load_pickle
from .helper.data_transformations import normalize_minmax, denormalize
from .helper.keras_pickle_compatible import make_keras_picklable


make_keras_picklable()


def build_autoencoder_layers(input_data: pd.DataFrame, latent_dimension: int):
    number_sensors = input_data.values.shape[1]
    if latent_dimension == 0:
        latent_dimension = int(0.5 * number_sensors)

    # this is our input placeholder
    input_layer = keras.layers.Input(shape=(number_sensors,))
    # "encoded" is the encoded representation of the input
    encoded = keras.layers.Dense(latent_dimension, activation='relu')(input_layer)
    # "decoded" is the lossy reconstruction of the input
    decoded = keras.layers.Dense(number_sensors, activation='sigmoid')(encoded)

    # this model maps an input to its reconstruction
    autoencoder = keras.models.Model(input_layer, decoded)
    # autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
    autoencoder.compile(optimizer='adadelta', loss='mse')
    return autoencoder


# based on https://blog.keras.io/building-autoencoders-in-keras.html
class Autoenc():
    def __init__(self, latent_space_size: int = 3, default_number_epochs: int = 100):
        self.latent_space_size = latent_space_size
        self.default_number_epochs = default_number_epochs
        self.reset()

    def reset(self):
        self.model = None
        self.scaler = None
        self.total_examples_trained = 0
        return self

    def fit(self, x: Union[np.ndarray, pd.DataFrame], y: Union[np.ndarray, pd.DataFrame] = None, w: Union[np.ndarray, pd.DataFrame] = None,
            number_epochs: int = 0, verbose_level: int = 0):

        if isinstance(x, np.ndarray):
            x = pd.DataFrame(x)

        x_norm, self.scaler = normalize_minmax(x)

        if number_epochs == 0:
            number_epochs = self.default_number_epochs

        # the actual model fit
        if self.model is None:
            self.model = build_autoencoder_layers(input_data=x_norm, latent_dimension=self.latent_space_size)

        training_data = x_norm.values.astype('float32')

        self.model.fit(training_data, training_data, epochs=number_epochs, batch_size=32, shuffle=False, verbose=verbose_level)
        self.total_examples_trained += training_data.shape[0] * number_epochs

        return self

    def predict(self, x: Union[np.ndarray, pd.DataFrame]):
        was_array = False
        if isinstance(x, np.ndarray):
            was_array = True
            x = pd.DataFrame(x)
        normalized_input, _ = normalize_minmax(x, self.scaler)

        estimation = self.model.predict(normalized_input.values)

        if was_array:
            estimation = denormalize(pd.DataFrame(estimation), self.scaler)
            return estimation.values
        else:   # (input was dataframe)
            estimation = denormalize(pd.DataFrame(estimation, index=x.index, columns=x.columns), self.scaler)
            return estimation

    def save(self, path: Path = None) -> Union[Path, List[Path]]:
        io_dict = {'model': self.model,
                   'latent_space_size': self.latent_space_size,
                   'default_number_epochs': self.default_number_epochs,
                   'total_examples_trained': self.total_examples_trained
                   }
        save_pickle(io_dict, Path(Path(path).as_posix() + '.pkl'))

    def load(self, path: Path):
        io_dict = load_pickle(Path(Path(path).as_posix() + '.pkl'))
        self.model = io_dict['model']
        self.latent_space_size = io_dict['latent_space_size']
        self.default_number_epochs = io_dict['default_number_epochs']
        self.total_examples_trained = io_dict['total_examples_trained']
        return self
