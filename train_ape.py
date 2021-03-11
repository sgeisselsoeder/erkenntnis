from os import listdir
from os.path import isfile, join
import numpy as np
from erkenntnis.brain_implementation.ai.world_model import Worldmodel

ape_brain = Worldmodel()

ending = ".pkl"
model_file = "ape_brain"
try:
    ape_brain.model.load(path=model_file)
    print("Trained on ", ape_brain.model.total_examples_trained, " examples")
except FileNotFoundError:
    print("Starting training a new model")

log_path = "./"
log_files = [f for f in listdir(log_path) if isfile(join(log_path, f)) and ".npy" in f and "monkey" in f]

# TODO: load all logs at once, train at once, more epochs

for logfile in log_files:
    print(logfile)
    logdata = np.loadtxt(logfile)
    ape_brain.train(logdata, epochs=1000, verbose_level=0)
    ape_brain.train(logdata, epochs=1, verbose_level=1)

ape_brain.model.save(path=model_file)
