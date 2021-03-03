from ..behavior_simple_memory import Behavior_simple_memory
from ..world_actions import *
from ..analyze_perception import split_perception_by_type
from ..utils import random_position, vector_length


class Behavior_wolf_hardcode(Behavior_simple_memory):
    def __init__(self, action_distance: float):
        super().__init__(memory_length=100)
        self.current_target_direction = None
        self.action_distance = action_distance

    def think(self, perception, messages):
        action = None
        action_cause = None

        for message in messages:
            if message["message"] == "malus":
                action = action_remove_malus()
                action_cause = message["from"]

        # TODO: react to other messages as well

        # Without messages, we analze what we see
        split_perception = split_perception_by_type(perception=perception)

        if "sheep" in split_perception:
            nearest_sheep = split_perception["sheep"][0]
            direction_to_nearest = nearest_sheep.position

            eating_distance = self.action_distance
            current_distance = vector_length(direction_to_nearest)
            if current_distance < eating_distance:
                action = action_eat(direction=direction_to_nearest)
            else:
                action = action_accelerate(direction=direction_to_nearest)
            action_cause = nearest_sheep.unique_properties

        elif "wolf" in split_perception:
            for wolf in split_perception["wolf"]:
                if wolf.malus:
                    action = action_inform_malus(direction=wolf.position)
                    action_cause = wolf.unique_properties
                    break
            if action is None:
                nearest_wolf = split_perception["wolf"][0]
                action = action_accelerate(direction=nearest_wolf.velocity)
                action_cause = nearest_wolf.unique_properties

        else:
            # we might want to keep a direction, but random for now
            self.current_target_direction = random_position()
            action = action_accelerate(direction=self.current_target_direction)

        self._remember(perception=perception, messages=messages, action=action, action_cause=action_cause)
        return action
