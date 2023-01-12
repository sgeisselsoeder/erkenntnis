import time
import visualizer
from visualizer import window
from erkenntnis.world import World
from erkenntnis.utils import random_position
from erkenntnis.things_available import *
from erkenntnis.agents_available import *


initial_world_scale = 100
map_boundary = 1.6 * initial_world_scale
map_resolution = 80

my_world = World(world_scale=initial_world_scale, malus_propability=0.0)
#my_world.add(new_stone(position=None))
# my_world.add(new_dummy_agent(position=None))

for i in range(300):
    my_world.add(new_grass(), position=random_position(scale=initial_world_scale))

for i in range(100):
    my_world.add(new_stone(), position=random_position(scale=initial_world_scale))


for i in range(40):
    my_world.add(new_sheep(), position=random_position(scale=0.8*initial_world_scale))

for i in range(8):
    my_world.add(new_wolf(), position=random_position(scale=0.6*initial_world_scale))

#for i in range(5):
#    my_world.add(new_monkey(log=True), position=random_position(scale=0.4*initial_world_scale))

#for i in range(10):
#    my_world.add(new_dummy_agent(), position=random_position(scale=initial_world_scale))


time.sleep(2)


window.start_world(my_world)
