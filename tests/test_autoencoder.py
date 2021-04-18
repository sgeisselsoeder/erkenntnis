from tensorflow.keras.datasets import fashion_mnist
import numpy as np
from matplotlib import pyplot as plt
from erkenntnis.brain_implementation.ai.autoencoder import Autoencoder


def test_autoencoding():
    number_pixels = 20
    data = np.zeros(shape=(1024, number_pixels), dtype=np.float32)
    data[:, 5] = 1.0
    data[::2, 2] = 1.0

    ae = Autoencoder(latent_space_size=3)
    ae.fit(x=data, number_epochs=20)

    for i in range(10):
        next_image = np.reshape(data[i], newshape=(1, number_pixels))
        result = ae.predict(next_image)
        print(np.sum(np.abs(result - next_image)) / number_pixels)


# # Import data
# (x_train, _), (x_test, _) = fashion_mnist.load_data()

# def reshape_and_normalize(data):
#     data = data.astype('float32') / 255.
#     data = data.reshape((len(data), np.prod(data.shape[1:])))
#     return data

# # Prepare input
# x_train = reshape_and_normalize(x_train)
# x_test = reshape_and_normalize(x_test)

# # train Autoencoder
# ae = Autoencoder(latent_space_size=8)
# try:
#     ae.load("autoencoder_newtype_8eng_60epochs.pkl")

# except FileNotFoundError as e:
#     ae.fit(x=x_train, number_epochs=60, input_test=x_test)
#     ae.save("autoencoder_newtype_8eng_60epochs.pkl")

# encoded_imgs = ae.encode(x_test)
# decoded_imgs = ae.decode(encoded_imgs)

# for i in range(len(x_test[:100])):
#     number_pixels = x_test[i].shape[0]
#     next_image = np.reshape(x_test[i], newshape=(1, number_pixels))
#     result = ae.predict(next_image)
#     print(np.sum(np.abs(result - next_image)) / number_pixels)

# # Keras implementation results
# plt.figure(figsize=(20, 4))
# for i in range(10):
#     # Original
#     subplot = plt.subplot(2, 10, i + 1)
#     plt.imshow(x_test[i].reshape(28, 28))
#     plt.gray()
#     subplot.get_xaxis().set_visible(False)
#     subplot.get_yaxis().set_visible(False)

#     # Reconstruction
#     subplot = plt.subplot(2, 10, i + 11)
#     plt.imshow(decoded_imgs[i].reshape(28, 28))
#     plt.gray()
#     subplot.get_xaxis().set_visible(False)
#     subplot.get_yaxis().set_visible(False)

# plt.show()
