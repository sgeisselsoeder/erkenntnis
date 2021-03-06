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

for i in range(10):
    for j in range(10):
        my_world.add(new_grass(), position=np.array([-20 + 4*i, -20 + 4*j, 0.0]))

for i in range(10):
    my_world.add(new_stone(), position=np.array([-20 + 4*i, -20, 0.0]))
    my_world.add(new_stone(), position=np.array([-20 + 4*i, 20, 0.0]))
    my_world.add(new_stone(), position=np.array([20, -20 + 4*i, 0.0]))

for i in range(4):
    my_world.add(new_stone(), position=np.array([-20 - 4*i, -20 + 4*i, 0.0]))
    my_world.add(new_stone(), position=np.array([-20 - 4*i,  20 - 4*i, 0.0]))

my_world.add(new_stone(), position=np.array([20, 20, 0.0]))

for i in range(30):
    my_world.add(new_grass(), position=random_position(scale=initial_world_scale))

for i in range(3):
    my_world.add(new_wolf(), position=random_position(scale=0.6*initial_world_scale))

for i in range(10):
    my_world.add(new_sheep(), position=random_position(scale=0.8*initial_world_scale))

my_world.print()
my_world.map(resolution=map_resolution, fixed_boundary=map_boundary, plotstyle="dense")
