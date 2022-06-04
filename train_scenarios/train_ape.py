from os import listdir
from os.path import isfile, join
import numpy as np
from erkenntnis.brain_implementation.ai.world_model import Worldmodel
from matplotlib import pyplot as plt


latent_space_size = 7

ape_brain = Worldmodel(latent_space_size=latent_space_size)

ending = ".pkl"
model_file = "ape_brain_" + str(latent_space_size)
try:
    ape_brain.model.load(path=model_file)
    print("Trained on ", ape_brain.model.total_examples_trained, " examples")
except FileNotFoundError:
    print("Starting training a new model")

log_path = "./"
log_files = [f for f in listdir(log_path) if isfile(join(log_path, f)) and ".npy" in f and "monkey" in f]
# log_files = [f for f in listdir(log_path) if isfile(join(log_path, f)) and ".npy" in f and "dummy" in f]

# TODO: load all logs at once, train at once, more epochs

for logfile in log_files:
    print(logfile)
    logdata = np.loadtxt(logfile)
    ape_brain.train(logdata, epochs=500, verbose_level=0)
    ape_brain.train(logdata, epochs=1, verbose_level=1)

    autoencoder = ape_brain.model

    encoded_imgs = autoencoder.encode(logdata)
    decoded_imgs = autoencoder.decode(encoded_imgs)

    # # Keras implementation results
    # plt.figure(figsize=(20, 4))
    # for i in range(9):
    #     # Original
    #     subplot = plt.subplot(2, 10, i + 1)
    #     plt.imshow(logdata[i].reshape(281, 1))
    #     plt.gray()
    #     subplot.get_xaxis().set_visible(False)
    #     subplot.get_yaxis().set_visible(False)

    #     # Reconstruction
    #     subplot = plt.subplot(2, 10, i + 11)
    #     plt.imshow(decoded_imgs[i].reshape(281, 1))
    #     plt.gray()
    #     subplot.get_xaxis().set_visible(False)
    #     subplot.get_yaxis().set_visible(False)

    # plt.show()


ape_brain.model.save(path=model_file + "_trained" + str(latent_space_size))
ape_brain.model.save(path=model_file)
