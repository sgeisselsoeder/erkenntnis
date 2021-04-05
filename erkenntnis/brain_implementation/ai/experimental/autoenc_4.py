# https://rubikscode.net/2018/11/26/3-ways-to-implement-autoencoders-with-tensorflow-and-python/

# from autoencoder_convonutional import Autoencoder
import matplotlib.pyplot as plt
# from autoencoder_keras import Autoencoder
from tensorflow.keras.datasets import fashion_mnist
import numpy as np
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.models import Model


class Autoencoder(object):

    def __init__(self):

        # Encoding
        input_layer = Input(shape=(28, 28, 1))
        encoding_conv_layer_1 = Conv2D(
            16, (3, 3), activation='relu', padding='same')(input_layer)
        encoding_pooling_layer_1 = MaxPooling2D(
            (2, 2), padding='same')(encoding_conv_layer_1)
        encoding_conv_layer_2 = Conv2D(
            8, (3, 3), activation='relu', padding='same')(encoding_pooling_layer_1)
        encoding_pooling_layer_2 = MaxPooling2D(
            (2, 2), padding='same')(encoding_conv_layer_2)
        encoding_conv_layer_3 = Conv2D(
            8, (3, 3), activation='relu', padding='same')(encoding_pooling_layer_2)
        code_layer = MaxPooling2D(
            (2, 2), padding='same')(encoding_conv_layer_3)

        # Decoding
        decodging_conv_layer_1 = Conv2D(
            8, (3, 3), activation='relu', padding='same')(code_layer)
        decodging_upsampling_layer_1 = UpSampling2D(
            (2, 2))(decodging_conv_layer_1)
        decodging_conv_layer_2 = Conv2D(8, (3, 3), activation='relu', padding='same')(
            decodging_upsampling_layer_1)
        decodging_upsampling_layer_2 = UpSampling2D(
            (2, 2))(decodging_conv_layer_2)
        decodging_conv_layer_3 = Conv2D(16, (3, 3), activation='relu')(
            decodging_upsampling_layer_2)
        decodging_upsampling_layer_3 = UpSampling2D(
            (2, 2))(decodging_conv_layer_3)
        output_layer = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(
            decodging_upsampling_layer_3)

        self._model = Model(input_layer, output_layer)
        self._model.compile(optimizer='adadelta', loss='binary_crossentropy')

    def train(self, input_train, input_test, batch_size, epochs):
        self._model.fit(input_train,
                        input_train,
                        epochs=epochs,
                        batch_size=batch_size,
                        shuffle=True,
                        validation_data=(
                            input_test,
                            input_test))

    def getDecodedImage(self, encoded_imgs):
        decoded_image = self._model.predict(encoded_imgs)
        return decoded_image


# Import data
(x_train, _), (x_test, _) = fashion_mnist.load_data()

# Prepare input
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))
x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))

# Convolutional implementation
autoencoder = Autoencoder()
autoencoder.train(x_train, x_test, 256, 50)
decoded_imgs = autoencoder.getDecodedImage(x_test)

# Convolutional implementation results
plt.figure(figsize=(20, 4))
for i in range(10):
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
