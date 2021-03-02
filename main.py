from erkenntnis.world import *


my_world = World()
my_world.add_thing(get_stone(position=None))
my_world.add_thing(get_grass(position=None))
my_world.add_agent(get_dummy_agent(position=None))
my_world.add_agent(get_sheep_agent(position=None))
# my_world.add_agent(get_wolf_agent(position=None))
# my_world.add_agent(get_ape_agent(position=None))

my_world.print()
my_world.map(resolution=40)

for i in range(100):
    my_world.run(time_delta=0.1)

my_world.print()
my_world.map(resolution=40)
