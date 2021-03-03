from erkenntnis.things_available import *
from erkenntnis.agents_available import *
from erkenntnis.utils import random_position


def test_things():
    temp = new_stone(position=None)
    temp = new_grass(position=None)
    temp = new_mirror(position=None)


def test_agents():
    temp = new_dummy_agent(position=None)
    temp = new_sheep(position=None)
    temp = new_wolf(position=None)
    temp = new_ape(position=None)


def test_thing_constructor_parameters():
    temp = new_grass(position=random_position())
    temp = new_grass(velocity=random_position())
    temp = new_grass(radius=5.0)


def _get_new_thing_type():
    thing = Thing(position=random_position(), velocity=random_position(), radius=100.0, health=500, max_speed=10.0)
    thing.friction = 0.5
    thing.type_properties = "magic_tool"
    return thing


def test_new_thing_type():
    thing = _get_new_thing_type()
