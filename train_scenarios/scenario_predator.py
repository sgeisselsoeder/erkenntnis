from erkenntnis.world import *

# This scenario is responsible to train agents to directly run away from predators
initial_world_scale = 10

my_world = World(world_scale=initial_world_scale)

my_world.add(new_monkey(log=True), position=np.array([0.0, -0.5, 0.0]))
my_world.add(new_wolf(log=True), position=np.array([0.5, 0.0, 0.0]))

for i in range(10):
    my_world.run(time_delta=0.3)
    my_world.map(resolution=80, fixed_boundary=initial_world_scale * 1.2, plotstyle="dense")
    # time.sleep(0.05)

my_world.print()
my_world.map(resolution=80, fixed_boundary=initial_world_scale * 1.2, plotstyle="dense")
