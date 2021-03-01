import numpy as np
from .agent import Behavior, action_accelerate


class Behavior_wolf_hardcode(Behavior):
    last_perceptions = []
    last_actions = []

    def think(self, perception):
        self.last_perceptions.append(perception)

        action = action_accelerate(direction=np.array([2.0 * np.random.random() - 1.0,
                                                       2.0 * np.random.random() - 1.0,
                                                       0.0]))
        self.last_actions.append(action)

        return action
