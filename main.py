import time
from erkenntnis.world import World
from erkenntnis.utils import random_position
from erkenntnis.things_available import *
from erkenntnis.agents_available import *


initial_world_scale = 100
map_boundary = 1.6 * initial_world_scale
map_resolution = 80

my_world = World(world_scale=initial_world_scale, malus_propability=0.0)
my_world.add(new_stone(position=None))
# my_world.add(new_dummy_agent(position=None))

for i in range(300):
    my_world.add(new_grass(), position=random_position(scale=initial_world_scale))

for i in range(40):
    my_world.add(new_sheep(), position=random_position(scale=0.8*initial_world_scale))

for i in range(3):
    my_world.add(new_wolf(), position=random_position(scale=0.6*initial_world_scale))

for i in range(5):
    my_world.add(new_monkey(log=True), position=random_position(scale=0.4*initial_world_scale))

for i in range(10):
    my_world.add(new_dummy_agent(), position=random_position(scale=initial_world_scale))

my_world.print()
my_world.map(resolution=map_resolution, fixed_boundary=map_boundary, plotstyle="dense")

time.sleep(2)

for i in range(3000):
    my_world.run(time_delta=0.3)
    # my_world.map(resolution=map_resolution, fixed_boundary=map_boundary, plotstyle="dense")
    if np.random.random() < 0.5:
        my_world.add(new_grass(), position=random_position(scale=initial_world_scale*1.8))
    my_world.map(resolution=map_resolution, fixed_boundary=map_boundary)

my_world.print()
my_world.map(resolution=map_resolution, fixed_boundary=map_boundary)
