import numpy as np
import uuid


class Thing:
    def __init__(self, position, velocity=np.array([0.0, 0.0, 0.0]), friction=0.01):
        self.position = position
        self.velocity = velocity
        self.friction = friction

        # any object is supposed to have properties unique to it's group and properties unique to itself
        self.type_properties = None     # could be equivalent to encoding of size of sheep, fur of wolf, number of limbs, ...

        # agents may perceive the unique properties of others, but not themselves (or maybe a subset)
        self.unique_properties = uuid.uuid1()       # could be equivalent to encoding of specific fur color, name, ...

    def move(self, dt):
        self.position = self.position + dt * self.velocity
        # friction
        self.velocity = self.velocity - self.velocity * dt * self.friction

    def accelerate(self, direction, dt):
        self.velocity = self.velocity + dt * direction
