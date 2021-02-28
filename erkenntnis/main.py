from .world import world


my_simulation = world()
world.add_thing()
world.add_thing()
world.add_thing()
world.add_thing()
world.add_thing()

world.add_agent()
world.add_agent()

for i in range(100):
    world.run(time_delta=0.1)

world.print()
