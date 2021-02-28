from .agent import Agent
from .behavior_dummy import behavior_dummy
from .behavior_sheep_hardcoded import behavior_sheep_hardcode
from .behavior_wolf_hardcoded import behavior_wolf_hardcode
from .behavior_ape_ml import behavior_ape_ml


def get_dummy_agent(position, velocity=None, radius=None, health: int = None, perception_radius=None):
    dummy = Agent(behavior=behavior_dummy, position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius)
    dummy.type_properties = "dummy"
    return dummy


def get_sheep_agent(position, velocity=None, radius=None, health: int = None, perception_radius=None):
    dummy = Agent(behavior=behavior_sheep_hardcode, position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius)
    dummy.type_properties = "sheep"
    return dummy


def get_wolf_agent(position, velocity=None, radius=None, health: int = None, perception_radius=None):
    dummy = Agent(behavior=behavior_wolf_hardcode, position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius)
    dummy.type_properties = "wolf"
    return dummy


def get_ape_agent(position, velocity=None, radius=None, health: int = None, perception_radius=None):
    dummy = Agent(behavior=behavior_ape_ml, position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius)
    dummy.type_properties = "ape"
    return dummy
