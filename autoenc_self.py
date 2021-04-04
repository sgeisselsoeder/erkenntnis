# https://rubikscode.net/2018/11/26/3-ways-to-implement-autoencoders-with-tensorflow-and-python/

# import matplotlib.pyplot as plt
# from autoencoder_keras import Autoencoder
from tensorflow.keras.datasets import fashion_mnist
import numpy as np
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Model
from matplotlib import pyplot as plt
# from .helper.pickle import save_pickle, load_pickle
from erkenntnis.brain_implementation.ai.helper.pickle import save_pickle, load_pickle
# from .helper.keras_pickle_compatible import make_keras_picklable
from erkenntnis.brain_implementation.ai.helper.keras_pickle_compatible import make_keras_picklable


make_keras_picklable()


class Autoencoder(object):

    def __init__(self, input_dim, encoded_dim):
        input_layer = Input(shape=(input_dim,))
        hidden_input = Input(shape=(encoded_dim,))
        hidden_layer = Dense(encoded_dim, activation='relu')(input_layer)
        output_layer = Dense(input_dim, activation='sigmoid')(hidden_layer)

        self._autoencoder_model = Model(input_layer, output_layer)

        self._encoder_model = Model(input_layer, hidden_layer)

        tmp_decoder_layer = self._autoencoder_model.layers[-1]
        self._decoder_model = Model(hidden_input, tmp_decoder_layer(hidden_input))

        # self._autoencoder_model.compile(optimizer='adadelta', loss='binary_crossentropy')
        self._autoencoder_model.compile(optimizer='adam', loss='mae')

    def train(self, input_train, epochs, input_test=None, batch_size=128):
        if input_test is None:
            validation_data = None
        else:
            validation_data = (input_test, input_test)
        self._autoencoder_model.fit(x=input_train, y=input_train,
                                    epochs=epochs, batch_size=batch_size,
                                    shuffle=True, validation_data=validation_data)

    def getEncodedImage(self, image):
        encoded_image = self._encoder_model.predict(image)
        return encoded_image

    def getDecodedImage(self, encoded_imgs):
        decoded_image = self._decoder_model.predict(encoded_imgs)
        return decoded_image

    def apply(self, image):
        return self.getDecodedImage(self.getEncodedImage(image))


# Import data
(x_train, _), (x_test, _) = fashion_mnist.load_data()

def reshape_and_normalize(data):
    data = data.astype('float32') / 255.
    data = data.reshape((len(data), np.prod(data.shape[1:])))    
    return data

# Prepare input
x_train = reshape_and_normalize(x_train)
x_test = reshape_and_normalize(x_test)

# Keras implementation


try:
    assert(False)
    autoencoder = load_pickle("autoencoder_16eng_200epochs_0.71mae_test.pkl")

except Exception:
    autoencoder = Autoencoder(input_dim=x_train.shape[1], encoded_dim=16)
    autoencoder.train(input_train=x_train, input_test=x_test, epochs=200)
    save_pickle(autoencoder, "autoencoder_16eng_200epochs.pkl")

encoded_imgs = autoencoder.getEncodedImage(x_test)
decoded_imgs = autoencoder.getDecodedImage(encoded_imgs)

for i in range(len(x_test[:100])):
    number_pixels = x_test[i].shape[0]
    next_image = np.reshape(x_test[i], newshape=(1, number_pixels))
    result = autoencoder.apply(next_image)
    print(np.sum(np.abs(result - next_image)) / number_pixels)

# Keras implementation results
plt.figure(figsize=(20, 4))
for i in range(9):
    # Original
    subplot = plt.subplot(2, 10, i + 1)
    plt.imshow(x_test[i].reshape(28, 28))
    plt.gray()
    subplot.get_xaxis().set_visible(False)
    subplot.get_yaxis().set_visible(False)

    # Reconstruction
    subplot = plt.subplot(2, 10, i + 11)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    plt.gray()
    subplot.get_xaxis().set_visible(False)
    subplot.get_yaxis().set_visible(False)

plt.show()
