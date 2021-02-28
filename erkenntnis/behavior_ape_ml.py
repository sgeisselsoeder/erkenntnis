import numpy as np
from .agent import Behavior, get_action_accelerate


class behavior_ape_ml(Behavior):
    last_perceptions = []
    last_actions = []

    def think(self, perception):
        self.old_perceptions.append(perception)

        action = get_action_accelerate(direction=[np.random.random(), np.random.random(), 0.0])
        self.last_actions.append(action)

        return action
