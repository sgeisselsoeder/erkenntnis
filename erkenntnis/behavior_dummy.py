import numpy as np
from .agent import Behavior, get_action_accelerate


class Behavior_dummy(Behavior):
    def __init__(self):
        self.last_perceptions = list()
        self.last_actions = list()

    def think(self, perception):
        self.last_perceptions.append(perception)

        action = get_action_accelerate(direction=np.array([np.random.random(), np.random.random(), 0.0]))
        self.last_actions.append(action)

        return action
