from ..brain_simple_memory import Brain_simple_memory
from ...world_actions import *
from ...utils import random_position


class Brain_ape_ml(Brain_simple_memory):
    def __init__(self, action_distance: float):
        super().__init__(memory_length=100)
        self.current_target_direction = None
        self.action_distance = action_distance
