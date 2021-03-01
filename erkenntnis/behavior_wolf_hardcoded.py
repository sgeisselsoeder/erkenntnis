from .agent import Behavior, action_accelerate
from .utils import random_position


class Behavior_wolf_hardcode(Behavior):
    last_perceptions = []
    last_actions = []

    def think(self, perception):
        self.last_perceptions.append(perception)

        action = action_accelerate(direction=random_position())
        self.last_actions.append(action)

        return action
