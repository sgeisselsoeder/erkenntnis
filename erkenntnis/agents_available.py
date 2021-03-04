import numpy as np
from .agent import Agent
from .brain_implementation.brain_dummy import Brain_dummy
from .brain_implementation.brain_sheep_hardcoded import Brain_sheep_hardcode
from .brain_implementation.brain_wolf_hardcoded import Brain_wolf_hardcode
from .brain_implementation.brain_ape_ml import Brain_ape_ml
from .brain_implementation.brain_monkey_hardcoded import Brain_monkey_hardcode
from .utils import random_position


def new_dummy_agent(position: np.ndarray = None, velocity=None, health: int = None):
    default_health = 100
    radius = 1.0
    max_speed = 3.0
    strength = 1.0
    perception_radius = 10.0

    if position is None:
        position = random_position()
    if health is None:
        health = default_health
    agent = Agent(behavior=Brain_dummy(), position=position, velocity=velocity,
                  radius=radius, default_health=health, perception_radius=perception_radius)
    agent.type_properties = "dummy"
    return agent


def new_sheep(position: np.ndarray = None, velocity=None, health: float = None):
    # sheep properties
    default_health = 80
    radius = 1.0
    max_speed = 1.5
    strength = 5.0
    perception_radius = 11.0

    if position is None:
        position = random_position()
    if health is None:
        health = default_health
    agent = Agent(behavior=Brain_sheep_hardcode(action_distance=max_speed), position=position, velocity=velocity,
                  radius=radius, default_health=health, perception_radius=perception_radius, max_speed=1.5, strength=strength)
    agent.type_properties = "sheep"
    return agent


def new_wolf(position: np.ndarray = None, velocity=None, health: float = None):
    # wolf properties
    default_health = 100
    radius = 1.0
    max_speed = 2.0
    strength = 10.0
    perception_radius = 10.0

    if position is None:
        position = random_position()
    if health is None:
        health = default_health
    agent = Agent(behavior=Brain_wolf_hardcode(action_distance=max_speed), position=position, velocity=velocity,
                  radius=radius, default_health=health, perception_radius=perception_radius, max_speed=max_speed, strength=strength)
    agent.type_properties = "wolf"
    return agent


def new_monkey(position: np.ndarray = None, velocity=None, health: float = None):
    # monkey and ape properties
    default_health = 80
    radius = 1.0
    max_speed = 2.5
    strength = 8.0
    perception_radius = 11.0

    if position is None:
        position = random_position()
    if health is None:
        health = default_health
    agent = Agent(behavior=Brain_monkey_hardcode(action_distance=max_speed), position=position, velocity=velocity,
                  radius=radius, default_health=health, perception_radius=perception_radius, max_speed=max_speed)
    agent.type_properties = "monkey"
    return agent


def new_ape(position: np.ndarray = None, velocity=None, health: float = None):
    agent = new_monkey(position=position, velocity=velocity, health=health)
    agent.behavior = Brain_ape_ml(action_distance=agent.max_speed)
    agent.type_properties = "ape"
    return agent
