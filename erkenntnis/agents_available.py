from .agent import Agent
from .behavior_dummy import Behavior_dummy
from .behavior_sheep_hardcoded import Behavior_sheep_hardcode
from .behavior_wolf_hardcoded import Behavior_wolf_hardcode
from .behavior_ape_ml import Behavior_ape_ml


def get_dummy_agent(position, velocity=None, radius=None, health: int = None, perception_radius=None):
    dummy = Agent(behavior=Behavior_dummy(), position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius)
    dummy.type_properties = "dummy"
    return dummy


def get_sheep_agent(position, velocity=None, radius=None, health: int = None, perception_radius=None):
    dummy = Agent(behavior=Behavior_sheep_hardcode(), position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius)
    dummy.type_properties = "sheep"
    return dummy


def get_wolf_agent(position, velocity=None, radius=None, health: int = None, perception_radius=None):
    dummy = Agent(behavior=Behavior_wolf_hardcode(), position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius)
    dummy.type_properties = "wolf"
    return dummy


def get_ape_agent(position, velocity=None, radius=None, health: int = None, perception_radius=None):
    dummy = Agent(behavior=Behavior_ape_ml(), position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius)
    dummy.type_properties = "ape"
    return dummy
