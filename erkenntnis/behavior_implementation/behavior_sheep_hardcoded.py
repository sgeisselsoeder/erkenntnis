from ..behavior_simple_memory import Behavior_simple_memory
from ..world_actions import *
from ..analyze_perception import split_perception_by_type
from ..utils import random_position, vector_length


class Behavior_sheep_hardcode(Behavior_simple_memory):
    def __init__(self, action_distance: float):
        super().__init__(memory_length=100)
        self.current_target_direction = None
        self.action_distance = action_distance

    def think(self, perception, messages):
        action = None
        action_cause = None
        split_perception = split_perception_by_type(perception=perception)

        if "wolf" in split_perception:
            nearest_wolf = split_perception["wolf"][0]
            direction_to_nearest = nearest_wolf.position
            action = action_accelerate(direction=-1.0 * direction_to_nearest)
            action_cause = nearest_wolf.unique_properties

        # TODO: maybe inform other sheep about malus?
        # elif "sheep" in split_perception:

        elif "grass" in split_perception:
            nearest_grass = split_perception["grass"][0]
            direction_to_nearest = nearest_grass.position
            eating_distance = self.action_distance
            current_distance = vector_length(direction_to_nearest)
            if current_distance < eating_distance:
                action = action_eat(direction=direction_to_nearest)
            else:
                action = action_accelerate(direction=direction_to_nearest)
            action_cause = nearest_grass.unique_properties

        else:
            # we might want to keep a direction, but random for now
            self.current_target_direction = random_position()
            action = action_accelerate(direction=self.current_target_direction)

        self._remember(perception=perception, messages=messages, action=action, action_cause=action_cause)
        return action