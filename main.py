import time
from erkenntnis.world import World
from erkenntnis.utils import random_position
from erkenntnis.things_available import *
from erkenntnis.agents_available import *

initial_world_scale = 100

my_world = World(world_scale=initial_world_scale, malus_propability=0.0)
my_world.add(new_stone(position=None))
# my_world.add(new_dummy_agent(position=None))

for i in range(300):
    my_world.add(new_grass(), position=random_position(scale=initial_world_scale))

for i in range(20):
    my_world.add(new_sheep(), position=random_position(scale=0.8*initial_world_scale))

for i in range(3):
    my_world.add(new_wolf(), position=random_position(scale=0.6*initial_world_scale))

for i in range(5):
    my_world.add(new_monkey(), position=random_position(scale=0.7*initial_world_scale))

my_world.print()
my_world.map(resolution=80, fixed_boundary=initial_world_scale * 1.2)

time.sleep(2)

for i in range(1000):
    my_world.run(time_delta=0.3)
    my_world.map(resolution=80, fixed_boundary=initial_world_scale * 1.2)

my_world.print()
my_world.map(resolution=80, fixed_boundary=initial_world_scale * 1.2)
