from .brain_simple_memory import Brain_simple_memory
from ..world_actions import *
from .preprocess_perception import split_perception_by_type
from ..utils import random_position, vector_length
from .ai_action_interface import action_to_numeric_encoding
from .ai_perception_interface import decode_perception
from .ai_message_interface import decode_messages


class Brain_wolf_hardcode(Brain_simple_memory):
    def __init__(self, action_distance: float, logfile: str = None):
        super().__init__(memory_length=100, logfile=logfile)
        self.current_target_direction = None
        self.action_distance = action_distance

    def _hunt(self, prey):
        direction_to_nearest = prey.position

        eating_distance = self.action_distance
        current_distance = vector_length(direction_to_nearest)
        if current_distance < eating_distance:
            action = action_eat(direction=direction_to_nearest)
        else:
            action = action_accelerate(direction=direction_to_nearest)
        cause = prey.unique_properties
        return action, cause

    def think(self, encoded_perception, encoded_messages):
        perception = decode_perception(encoded_perception)
        messages = decode_messages(encoded_messages)
        action = None
        cause = None

        for message in messages:
            if message["message"] == "malus":
                action = action_remove_malus()
                cause = message["from"]

        # TODO: react to other messages as well

        # Without messages, we analyze what we see
        split_perception = split_perception_by_type(perception=perception)

        # favored prey
        for prey_category in ["sheep", "monkey", "ape"]:
            if action is None and prey_category in split_perception:
                nearest_prey = split_perception[prey_category][0]
                action, cause = self._hunt(nearest_prey)
                break

        if action is None and "wolf" in split_perception:
            for wolf in split_perception["wolf"]:
                if wolf.malus:
                    action = action_inform_malus(direction=wolf.position)
                    cause = wolf.unique_properties
                    break
            if action is None:
                nearest_wolf = split_perception["wolf"][0]
                action = action_accelerate(direction=nearest_wolf.velocity)
                cause = nearest_wolf.unique_properties

        if action is None:
            # we might want to keep a direction, but random for now
            self.current_target_direction = random_position()
            action = action_accelerate(direction=self.current_target_direction)
            # wolf must be predictable, no random action!

        self._remember(perception=perception, messages=messages, action=action, cause=cause)
        encoded_action = action_to_numeric_encoding(action=action)
        return encoded_action, cause
