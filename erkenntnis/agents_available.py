from .agent import Agent
from .behavior_sheep_hardcoded import behavior_sheep_hardcode


class Sheep(Agent):
    def __init__(self, behavior, position, velocity=None, radius=None, health: int = None, perception_radius=None):
        super().__init__(behavior=behavior_sheep_hardcode, position=position, velocity=velocity, radius=radius,
                         health=health, perception_radius=perception_radius)
        self.type_properties = "sheep"


class Wolf(Agent):
    def __init__(self, position, velocity=None, radius=None):
        super().__init__(behavior=None, position=position, velocity=velocity, radius=radius)
        self.type_properties = "wolf"


class Ape_ML(Agent):
    def __init__(self, position, velocity=None, radius=None):
        super().__init__(behavior=None, position=position, velocity=velocity, radius=radius)
        self.type_properties = "ape"
