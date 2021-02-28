import numpy as np
from .thing import Thing


def get_action_accelerate(direction, strength=1.0):
    return {"type": "accelerate",
            "direction": direction,
            "strength": strength}


class Behavior:
    def think(self, perception):
        action = get_action_accelerate(direction=np.array([np.random.random(), np.random.random(), 0.0]))
        return action


def get_random_agent():
    random_behavior = Behavior()
    return Agent(behavior=random_behavior, position=np.array([np.random.random(), np.random.random(), 0.0]))


class Agent(Thing):
    behavior = None
    perception_radius = 10

    def __init__(self, behavior, position, velocity=np.array([0.0, 0.0, 0.0])):
        self.behavior = behavior
        super().__init__(position=position, velocity=velocity)

    # below are possibly allowed actions
    def action_talk(self, agent, message):
        pass

    def action_notify(self, agent, direction):
        # alternatively also target agent
        pass

    def action_accelerate(self, direction, strength):
        return None

    def action_interact(self, direction):
        return None

    def action_attack(self, direction):
        return None

    def action_benefit(self, direction):
        return None

    def action_benefit_self(self):
        return None

    def action_focus(self, direction):
        # gain in depth perception
        return None
