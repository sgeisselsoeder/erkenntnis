from erkenntnis.world import World


my_world = World()
my_world.add_thing()
my_world.add_thing()
my_world.add_thing()
my_world.add_thing()
my_world.add_thing()

my_world.add_agent()
my_world.add_agent()

my_world.print()

for i in range(100):
    my_world.run(time_delta=0.1)

my_world.print()
