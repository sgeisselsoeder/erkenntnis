import numpy as np
import uuid
from .utils import random_position, normalize_vector_3d


class Thing:
    def __init__(self, position, velocity=None, radius=None, friction=None, health=None):
        _default_velocity = np.array([0.0, 0.0, 0.0])
        _default_radius = 1.0
        _default_friction = 0.01

        self.position = position
        if self.position is None:
            self.position = random_position()

        self.velocity = velocity
        if self.velocity is None:
            self.velocity = _default_velocity
        self.radius = radius
        if self.radius is None:
            self.radius = _default_radius
        self.friction = friction
        if self.friction is None:
            self.friction = _default_friction

        self.malus = False

        self.health = 100
        if health is not None:
            self.health = health

        # any object is supposed to have properties unique to it's group and properties unique to itself
        # could be equivalent to encoding of size of sheep, fur of wolf, number of limbs, ...
        self.type_properties = "thing"

        # agents may perceive the unique properties of others, but not themselves (or maybe a subset)
        # could be equivalent to encoding of individual specific fur color, name, eye color, ...
        self.unique_properties = uuid.uuid1()

    def move(self, dt):
        self.position = self.position + dt * self.velocity
        # friction
        self.velocity = self.velocity - self.velocity * dt * self.friction

    def accelerate(self, direction, dt, strength: float = 1.0):
        normalized_direction = normalize_vector_3d(direction)
        real_strength = np.min(np.abs(strength), 1.0)
        self.velocity = self.velocity + dt * normalized_direction * real_strength

    def __str__(self):
        return str(self.type_properties) + " at " + str(self.position)
