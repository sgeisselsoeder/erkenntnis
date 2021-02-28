import numpy as np
from .thing import thing


def acceleration_action(direction, strength=1.0):
    return {"type": "accelerate",
            "direction": direction,
            "strength": strength}


class behavior:
    def think(self, perception):
        action = acceleration_action(direction=[np.random(), np.random(), 0.0])
        return action


class agent(thing):
    behavior = None
    perception_radius = 10

    def __init__(self, behavior, position, velocity=None):
        self.behavior = behavior
        super().__init__(position=position, velocity=velocity)

    # below are possibly allowed actions

    def accelerate(self, direction, strength):
        return None

    def interact(self, direction):
        return None

    def attack(self, direction):
        return None

    def benefit(self, direction):
        return None

    def benefit_self(self):
        return None

    def focus(self, direction):
        # gain in depth perception
        return None
