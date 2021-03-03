import numpy as np
from .thing import Thing
from .utils import random_position


class Stone(Thing):
    def __init__(self, position, velocity=None, radius=None):
        super().__init__(position=position, velocity=velocity, radius=radius, health=500)
        self.type_properties = "stone"


def new_stone(position: np.ndarray = None, velocity=None, radius=None):
    if position is None:
        position = random_position()
    return Stone(position=position, velocity=velocity, radius=radius)


class Grass(Thing):
    def __init__(self, position, velocity=None, radius=None):
        super().__init__(position=position, velocity=velocity, radius=radius, health=10)
        self.type_properties = "grass"


def new_grass(position: np.ndarray = None, velocity=None, radius=None):
    if position is None:
        position = random_position()
    return Grass(position=position, velocity=velocity, radius=radius)


class Mirror(Thing):
    def __init__(self, position, velocity=None, radius=None):
        super().__init__(position=position, velocity=velocity, radius=radius, health=500)
        self.type_properties = "mirror"


def new_mirror(position: np.ndarray = None, velocity=None, radius=None):
    if position is None:
        position = random_position()
    return Mirror(position=position, velocity=velocity, radius=radius)
