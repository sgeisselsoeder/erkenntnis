# https://rubikscode.net/2018/11/26/3-ways-to-implement-autoencoders-with-tensorflow-and-python/

# import matplotlib.pyplot as plt
# from autoencoder_keras import Autoencoder
from tensorflow.keras.datasets import fashion_mnist
import numpy as np
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Model
from matplotlib import pyplot as plt


class Autoencoder(object):

    def __init__(self, inout_dim, encoded_dim):
        input_layer = Input(shape=(inout_dim,))
        hidden_input = Input(shape=(encoded_dim,))
        hidden_layer = Dense(encoded_dim, activation='relu')(input_layer)
        output_layer = Dense(784, activation='sigmoid')(hidden_layer)

        self._autoencoder_model = Model(input_layer, output_layer)
        self._encoder_model = Model(input_layer, hidden_layer)
        tmp_decoder_layer = self._autoencoder_model.layers[-1]
        self._decoder_model = Model(hidden_input, tmp_decoder_layer(hidden_input))

        self._autoencoder_model.compile(optimizer='adadelta', loss='binary_crossentropy')

    def train(self, input_train, input_test, batch_size, epochs):
        self._autoencoder_model.fit(input_train,
                                    input_train,
                                    epochs=epochs,
                                    batch_size=batch_size,
                                    shuffle=True,
                                    validation_data=(
                                        input_test,
                                        input_test))

    def getEncodedImage(self, image):
        encoded_image = self._encoder_model.predict(image)
        return encoded_image

    def getDecodedImage(self, encoded_imgs):
        decoded_image = self._decoder_model.predict(encoded_imgs)
        return decoded_image


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
autoencoder = Autoencoder(inout_dim=x_train.shape[1], encoded_dim=32)
autoencoder.train(input_train=x_train, input_test=x_test, batch_size=256, epochs=20)
encoded_imgs = autoencoder.getEncodedImage(x_test)
decoded_imgs = autoencoder.getDecodedImage(encoded_imgs)

# Keras implementation results
plt.figure(figsize=(20, 4))
for i in range(6):
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
