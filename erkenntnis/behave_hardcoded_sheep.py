from .agent import *


class agent_hardcode_wolf(behavior):
    last_perceptions = []
    last_actions = []

    def think_and_act(self, perception):
        self.old_perceptions.append(perception)

        action = acceleration_action(direction=[np.random(), np.random(), 0.0])
        self.last_actions.append(action)

        return action
