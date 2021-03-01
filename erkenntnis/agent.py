import numpy as np
from .thing import Thing


def action_accelerate(direction, strength=1.0):
    return {"type": "accelerate",
            "direction": direction,
            "strength": strength}


class Behavior:
    def think(self, perception):
        return None


class Agent(Thing):
    def __init__(self, behavior, position, velocity=None, radius=None, health: int = None, perception_radius=None):
        super().__init__(position=position, velocity=velocity, radius=radius, health=health)

        self.behavior = behavior
        self.action_cooldown = 0

        self.default_perception_radius = 5
        if perception_radius is not None:
            self.default_perception_radius = perception_radius
        self.perception_radius = self.default_perception_radius

        # option to store received messages from other agents.
        # should be emptied by the world upon perceive() or by themselves at the beginning of think
        self.messages = list()

        # could be equivalent to encoding of size of sheep, fur of wolf, number of limbs, ...
        self.type_properties = "agent"

    def think(self, perception):
        return self.behavior.think(perception)
