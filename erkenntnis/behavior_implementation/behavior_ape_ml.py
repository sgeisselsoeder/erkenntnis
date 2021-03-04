from ..behavior_simple_memory import Behavior_simple_memory
from ..world_actions import *
from ..analyze_perception import split_perception_by_type
from ..utils import random_position


class Behavior_ape_ml(Behavior_simple_memory):
    def __init__(self, action_distance: float):
        super().__init__(memory_length=100)
        self.current_target_direction = None
        self.action_distance = action_distance
