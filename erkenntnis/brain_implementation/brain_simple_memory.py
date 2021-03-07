from .brain import Brain
from ..utils import random_position
from ..world_actions import action_accelerate
from .ai_action_interface import action_to_numeric_encoding


class Brain_simple_memory(Brain):
    def __init__(self, memory_length: int = 10):
        self.last_perceptions = list()
        self.last_actions = list()
        self.last_causes = list()
        self.last_messages = list()
        self.memory_length = memory_length
        # TODO: have a fixed length list of known agents. encode unique agent ids using that?
        self.known_agents = list()

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
        action = action_accelerate(direction=random_position())
        self._remember(perception=encoded_perception, messages=encoded_messages, action=action, cause=None)
        encoded_action = action_to_numeric_encoding(action=action)
        return encoded_action, None
