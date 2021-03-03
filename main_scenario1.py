from erkenntnis.world import *
from erkenntnis.utils import random_position
import time

initial_world_scale = 100

my_world = World(world_scale=initial_world_scale)

my_world.add(new_grass(), position=np.array([1.0, 0.0, 0.0]))

my_world.add(new_sheep(), position=np.array([1.0, 8.0, 0.0]))

my_world.add(new_wolf(velocity=np.array([3.0, 0.0, 0.0])), position=np.array([-18.0, -2.0, 0.0]))

my_world.print()
my_world.map(resolution=80, fixed_boundary=initial_world_scale * 1.2, plotstyle="dense")

for i in range(1000):
    my_world.run(time_delta=0.3)
    # print(my_world.time)
    # print(len(my_world.agents))
    my_world.map(resolution=80, fixed_boundary=initial_world_scale * 1.2, plotstyle="dense")
    time.sleep(0.05)

my_world.print()
my_world.map(resolution=80, fixed_boundary=initial_world_scale * 1.2, plotstyle="dense")
