from .world import World
from .things_available import *
from .agents_available import *


def add_stone(world: World, position, velocity=None, radius=None):
    world.add_thing(Stone(position=position, velocity=velocity, radius=radius))


def add_grass(world: World, position, velocity=None, radius=None):
    world.add_thing(Grass(position=position, velocity=velocity, radius=radius))


def add_mirror(world: World, position, velocity=None, radius=None):
    world.add_thing(Mirror(position=position, velocity=velocity, radius=radius))


def add_sheep(world: World, position, velocity=None, radius=None):
    world.add_agent(Sheep(position=position, velocity=velocity, radius=radius))
