from .things_available import *
from .agents_available import *


def add_stone(world, position, velocity=None, radius=None):
    world.add_thing(get_stone(position=position, velocity=velocity, radius=radius))


def add_grass(world, position, velocity=None, radius=None):
    world.add_thing(get_grass(position=position, velocity=velocity, radius=radius))


def add_mirror(world, position, velocity=None, radius=None):
    world.add_thing(get_mirror(position=position, velocity=velocity, radius=radius))


def add_dummy(world, position, velocity=None, radius=None):
    world.add_agent(get_dummy_agent(position=position, velocity=velocity, radius=radius))


def add_sheep(world, position, velocity=None, radius=None):
    world.add_agent(get_sheep_agent(position=position, velocity=velocity, radius=radius))


def add_wolf(world, position, velocity=None, radius=None):
    world.add_agent(get_wolf_agent(position=position, velocity=velocity, radius=radius))


def add_ape(world, position, velocity=None, radius=None):
    world.add_agent(get_ape_agent(position=position, velocity=velocity, radius=radius))
