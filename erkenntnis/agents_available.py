from .agent import Agent
from .behavior_dummy import Behavior_dummy
from .behavior_sheep_hardcoded import Behavior_sheep_hardcode
from .behavior_wolf_hardcoded import Behavior_wolf_hardcode
from .behavior_ape_ml import Behavior_ape_ml


def get_dummy_agent(position, velocity=None, radius=None, health: int = None, perception_radius=None, max_speed=3.0):
    agent = Agent(behavior=Behavior_dummy(), position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius)
    agent.type_properties = "dummy"
    return agent


def get_sheep_agent(position, velocity=None, radius=None, health: int = None, perception_radius=None, max_speed=1.5):
    agent = Agent(behavior=Behavior_sheep_hardcode(action_distance=max_speed), position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius, max_speed=1.5)
    agent.type_properties = "sheep"
    return agent


def get_wolf_agent(position, velocity=None, radius=None, health: int = None, perception_radius=None, max_speed=2.0):
    agent = Agent(behavior=Behavior_wolf_hardcode(action_distance=max_speed), position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius, max_speed=max_speed)
    agent.type_properties = "wolf"
    return agent


def get_ape_agent(position, velocity=None, radius=None, health: int = None, perception_radius=None, max_speed=2.5):
    agent = Agent(behavior=Behavior_ape_ml(action_distance=max_speed), position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius, max_speed=max_speed)
    agent.type_properties = "ape"
    return agent
