from .behavior_agent import Behavior
from .utils import random_position
from .world_actions import action_accelerate


class Behavior_simple_memory(Behavior):
    def __init__(self, memory_length: int = 10):
        self.last_perceptions = list()
        self.last_actions = list()
        self.memory_length = memory_length

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