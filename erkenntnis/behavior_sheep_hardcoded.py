from .agent import Behavior, action_accelerate
from .utils import random_position


class Behavior_sheep_hardcode(Behavior):
    def __init__(self):
        self.last_perceptions = list()
        self.last_actions = list()
        self.memory_length = 100

    def _remember(self, perception, action):
        self.last_perceptions.append(perception)
        self.last_actions.append(action)
        self._forget_old()

    def _forget_old(self):
        self.last_perceptions = self.last_perceptions[-self.memory_length:]
        self.last_actions = self.last_actions[-self.memory_length:]

    def think(self, perception):
        action = action_accelerate(direction=random_position())
        self._remember(perception=perception, action=action)
        return action
