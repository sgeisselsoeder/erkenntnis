from ..behavior_simple_memory import Behavior_simple_memory


class Behavior_dummy(Behavior_simple_memory):
    def __init__(self):
        super().__init__(memory_length=3)
