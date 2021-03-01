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
        super().__init__(position=position, velocity=velocity, radius=radius)

        _default_health = 100
        _default_perception_radius = 10

        self.behavior = behavior

        self.health = _default_health
        if health is not None:
            self.health = health
        self.perception_radius = _default_perception_radius
        if perception_radius is not None:
            self.perception_radius = perception_radius

        # option to store received messages from other agents.
        # should be emptied by the world upon perceive() or by themselves at the beginning of think
        self.messages = list()

        # could be equivalent to encoding of size of sheep, fur of wolf, number of limbs, ...
        self.type_properties = "agent"

    def think(self, perception):
        return self.behavior.think(perception)

    # # below are possibly allowed actions
    # def action_talk(self, agent, message):
    #     pass

    # def action_notify(self, agent, direction):
    #     # alternatively also target agent
    #     pass

    # def action_accelerate(self, direction, strength):
    #     return None

    # def action_interact(self, direction):
    #     return None

    # def action_attack(self, direction):
    #     return None

    # def action_benefit(self, direction):
    #     return None

    # def action_benefit_self(self):
    #     return None

    # def action_focus(self, direction):
    #     # gain in depth perception
    #     return None
