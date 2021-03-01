import numpy as np
from .agent import Behavior, action_accelerate


class Behavior_dummy(Behavior):
    def __init__(self):
        self.last_perceptions = list()
        self.last_actions = list()
        self.memory_length = 10

    def _remember(self, perception, action):
        self.last_perceptions.append(perception)
        self.last_actions.append(action)
        self._forget_old()

    def _forget_old(self):
        self.last_perceptions = self.last_perceptions[-self.memory_length:]
        self.last_actions = self.last_actions[-self.memory_length:]

    def think(self, perception):
        action = action_accelerate(direction=np.array([2.0 * np.random.random() - 1.0,
                                                           2.0 * np.random.random() - 1.0,
                                                           0.0]))        
        self._remember(perception=perception, action=action)
        return action
