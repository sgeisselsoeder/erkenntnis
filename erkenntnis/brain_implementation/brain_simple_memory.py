import numpy as np
from .brain import Brain
from .ai_action_interface import action_to_numeric_encoding
from ..available_actions import random_action


class Brain_simple_memory(Brain):
    def __init__(self, memory_length: int = 10, logfile: str = None):
        self.last_perceptions = list()
        self.last_actions = list()
        self.last_causes = list()
        self.last_messages = list()
        self.memory_length = memory_length
        # TODO: have a fixed length list of known agents. encode unique agent ids using that?
        # (forgetting old agents)
        self.known_agents = list()
        self.logfile = logfile
        # if logfile is not None:
        #     self.logfile = open(logfile, 'a+')

    def _remember(self, perception, messages, action, cause=None):
        # print(type(self), " ", action, " ", cause)
        self.last_perceptions.append(perception)
        self.last_actions.append(action)
        self.last_causes.append(cause)
        self.last_messages.append(messages)
        self._forget_old()

    def _forget_old(self):
        self.last_perceptions = self.last_perceptions[-self.memory_length:]
        self.last_actions = self.last_actions[-self.memory_length:]
        self.last_causes = self.last_causes[-self.memory_length:]
        self.last_messages = self.last_messages[-self.memory_length:]

    def think(self, encoded_perception, encoded_messages):
        action = random_action()
        encoded_action = action_to_numeric_encoding(action=action)
        self._remember(perception=encoded_perception, messages=encoded_messages, action=encoded_action, cause=None)
        return encoded_action, None

    def log(self):
        if self.logfile:
            last_cause = self.last_causes[-1]
            if last_cause is None:
                last_cause = np.array([0.0])
            logstate = np.concatenate([self.last_perceptions[-1], self.last_messages[-1],
                                       self.last_actions[-1], last_cause])
            logstate = np.reshape(logstate, (1, logstate.shape[0]))
            logfile = open(self.logfile, 'a+')
            np.savetxt(logfile, logstate)
            logfile.close()
