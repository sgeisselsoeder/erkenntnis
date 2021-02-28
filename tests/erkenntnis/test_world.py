from erkenntnis.world import World


def test_world():
    my_world = World()
    my_world.add_random_thing()
    my_world.add_random_thing()

    my_world.add_random_agent()
    my_world.add_random_agent()

    my_world.print()

    for i in range(10):
        my_world.run(time_delta=0.1)

    my_world.print()
