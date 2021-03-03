from erkenntnis.world import *
from erkenntnis.utils import random_position

initial_world_scale = 100

my_world = World(world_scale=initial_world_scale)

for i in range(200):
    my_world.add(new_grass(), position=random_position(scale=initial_world_scale))
my_world.add(new_grass(), position=random_position(scale=initial_world_scale))

my_world.add(new_sheep(), position=random_position(scale=0.8*initial_world_scale))

my_world.add(new_wolf(), position=random_position(scale=0.6*initial_world_scale))

my_world.print()
my_world.map(resolution=80, fixed_boundary=initial_world_scale * 1.2, plotstyle="dense")

for i in range(1000):
    my_world.run(time_delta=0.3)
    print(my_world.time)
    # print(len(my_world.agents))
    my_world.map(resolution=80, fixed_boundary=initial_world_scale * 1.2, plotstyle="dense")

my_world.print()
my_world.map(resolution=80, fixed_boundary=initial_world_scale * 1.2, plotstyle="dense")