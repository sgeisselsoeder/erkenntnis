from erkenntnis.world import *
from erkenntnis.utils import random_position

world_scale = 40

my_world = World()
my_world.add_thing(get_stone(position=None))
# my_world.add_agent(get_dummy_agent(position=None))

for i in range(1000):
    my_world.add_thing(get_grass(position=random_position(scale=world_scale)))

for i in range(100):
    my_world.add_thing(get_sheep_agent(position=random_position(scale=world_scale)))

for i in range(10):
    my_world.add_agent(get_wolf_agent(position=random_position(scale=world_scale)))

# my_world.add_agent(get_ape_agent(position=None))

my_world.print()
my_world.map(resolution=80)

for i in range(1000):
    my_world.run(time_delta=0.3)
    # print(my_world.time)
    my_world.map(resolution=80)

my_world.print()
my_world.map(resolution=80)
