import numpy as np
import pandas as pd
from pathlib import Path
from typing import Union, List

from tensorflow import keras
from .helper.pickle import save_pickle, load_pickle
from .helper.data_transformations import normalize_minmax, denormalize
from .helper.keras_pickle_compatible import make_keras_picklable
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Model


make_keras_picklable()


# def build_autoencoder_layers(input_data: pd.DataFrame, latent_dimension: int):
#     number_sensors = input_data.values.shape[1]
#     if latent_dimension == 0:
#         latent_dimension = int(0.5 * number_sensors)

#     # this is our input placeholder
#     input_layer = keras.layers.Input(shape=(number_sensors,))
#     # "encoded" is the encoded representation of the input
#     encoded = keras.layers.Dense(latent_dimension, activation='relu')(input_layer)
#     # "decoded" is the lossy reconstruction of the input
#     decoded = keras.layers.Dense(number_sensors, activation='sigmoid')(encoded)

#     # this model maps an input to its reconstruction
#     autoencoder = keras.models.Model(input_layer, decoded)
#     # autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
#     autoencoder.compile(optimizer='adadelta', loss='mse')
#     return autoencoder


# based on https://blog.keras.io/building-autoencoders-in-keras.html ...
# based now more on https://rubikscode.net/2018/11/26/3-ways-to-implement-autoencoders-with-tensorflow-and-python/
class Autoencoder():
    def _setup_autoencoder(self, input_dim, encoded_dim):
        input_layer = Input(shape=(input_dim,))
        hidden_input = Input(shape=(encoded_dim,))
        hidden_layer = Dense(encoded_dim, activation='relu')(input_layer)
        output_layer = Dense(input_dim, activation='sigmoid')(hidden_layer)

        self.autoencoder = Model(input_layer, output_layer)

        self.encoder = Model(input_layer, hidden_layer)

        tmp_decoder_layer = self.autoencoder.layers[-1]
        self.decoder = Model(hidden_input, tmp_decoder_layer(hidden_input))

        # self._autoencoder_model.compile(optimizer='adadelta', loss='binary_crossentropy')
        self.autoencoder.compile(optimizer='adam', loss='mae')

    def __init__(self, latent_space_size: int = 3, default_number_epochs: int = 100):
        self.latent_space_size = latent_space_size
        self.default_number_epochs = default_number_epochs
        self.reset()

    def reset(self):
        self.autoencoder = None
        self.encoder = None
        self.decoder = None
        self.scaler = None
        self.total_examples_trained = 0
        return self

    def encode(self, examples):
        encoded = self.encoder.predict(examples)
        return encoded

    def decode(self, encoded_examples):
        decoded_examples = self.decoder.predict(encoded_examples)
        return decoded_examples

    def fit(self, x: Union[np.ndarray, pd.DataFrame], y: Union[np.ndarray, pd.DataFrame] = None, w: Union[np.ndarray, pd.DataFrame] = None,
            number_epochs: int = 0, verbose_level: int = 0, input_test=None, batch_size=128):

        # make sure we have the network architecture in place
        if self.autoencoder is None:
            number_sensors = x.values.shape[1]
            if self.latent_space_size == 0:
                self.latent_space_size = int(0.1 * number_sensors)
            self._setup_autoencoder(input_dim=number_sensors, encoded_dim=self.latent_space_size)

        # preprocess the data for this model
        if isinstance(x, np.ndarray):
            x = pd.DataFrame(x)
        x_norm, self.scaler = normalize_minmax(x, self.scaler)  # if we already have a scaler, we want to reuse it? (else this doesn't change anything)
        training_data = x_norm.values.astype('float32')

        # sanitize training parameters
        if number_epochs <= 0:
            number_epochs = self.default_number_epochs
        if input_test is None:
            validation_data = None
        else:
            validation_data = (input_test, input_test)

        # fit the model to the data
        self.autoencoder.fit(x=training_data, y=training_data,
                             epochs=number_epochs, batch_size=batch_size,
                             shuffle=True, validation_data=validation_data)

        self.total_examples_trained += training_data.shape[0] * number_epochs

        return self

    def predict(self, x: Union[np.ndarray, pd.DataFrame]):
        was_array = False
        if isinstance(x, np.ndarray):
            was_array = True
            x = pd.DataFrame(x)
        normalized_input, _ = normalize_minmax(x, self.scaler)

        estimation = self.autoencoder.predict(normalized_input.values)
        # TODO: test is this is exactly the same
        # estimation = self.decode(self.encode(normalized_input.values))

        if was_array:
            estimation = denormalize(pd.DataFrame(estimation), self.scaler)
            return estimation.values
        else:   # (input was dataframe)
            estimation = denormalize(pd.DataFrame(
                estimation, index=x.index, columns=x.columns), self.scaler)
            return estimation

    def save(self, path: Path = None) -> Union[Path, List[Path]]:
        io_dict = {'autoencoder': self.autoencoder,
                   'encoder': self.encoder,
                   'decoder': self.decoder,
                   'latent_space_size': self.latent_space_size,
                   'default_number_epochs': self.default_number_epochs,
                   'total_examples_trained': self.total_examples_trained
                   }
        save_pickle(io_dict, Path(Path(path).as_posix() + '.pkl'))

    def load(self, path: Path):
        io_dict = load_pickle(Path(Path(path).as_posix() + '.pkl'))
        self.autoencoder = io_dict['autoencoder']
        self.encoder = io_dict['encoder']
        self.decoder = io_dict['decoder']
        self.latent_space_size = io_dict['latent_space_size']
        self.default_number_epochs = io_dict['default_number_epochs']
        self.total_examples_trained = io_dict['total_examples_trained']
        return self
