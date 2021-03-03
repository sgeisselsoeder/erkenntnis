import numpy as np
from .agent import Agent
from .behavior_dummy import Behavior_dummy
from .behavior_sheep_hardcoded import Behavior_sheep_hardcode
from .behavior_wolf_hardcoded import Behavior_wolf_hardcode
from .behavior_ape_ml import Behavior_ape_ml
from .utils import random_position


def new_dummy_agent(position: np.ndarray = None, velocity=None, radius=None, health: int = None, perception_radius=None, max_speed=3.0):
    if position is None:
        position = random_position()
    agent = Agent(behavior=Behavior_dummy(), position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius)
    agent.type_properties = "dummy"
    return agent


def new_sheep(position: np.ndarray = None, velocity=None, radius=None, health: int = None, perception_radius=None, max_speed=1.5):
    if position is None:
        position = random_position()
    agent = Agent(behavior=Behavior_sheep_hardcode(action_distance=max_speed), position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius, max_speed=1.5)
    agent.type_properties = "sheep"
    return agent


def new_wolf(position: np.ndarray = None, velocity=None, radius=None, health: int = None, perception_radius=None, max_speed=2.0):
    if position is None:
        position = random_position()
    agent = Agent(behavior=Behavior_wolf_hardcode(action_distance=max_speed), position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius, max_speed=max_speed)
    agent.type_properties = "wolf"
    return agent


def new_ape(position: np.ndarray = None, velocity=None, radius=None, health: int = None, perception_radius=None, max_speed=2.5):
    if position is None:
        position = random_position()
    agent = Agent(behavior=Behavior_ape_ml(action_distance=max_speed), position=position, velocity=velocity,
                  radius=radius, health=health, perception_radius=perception_radius, max_speed=max_speed)
    agent.type_properties = "ape"
    return agent
