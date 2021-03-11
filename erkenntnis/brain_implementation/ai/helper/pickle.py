import pickle
from pathlib import Path


def load_pickle(path):
    path = Path(path)
    with open(path, "rb") as file:
        return pickle.load(file)


def save_pickle(data, path, create_path=True):
    path = Path(path)
    if create_path:
        path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as file:
        pickle.dump(data, file)
    return path
