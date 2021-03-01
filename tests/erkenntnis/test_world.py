from erkenntnis.world import *


def _setup_world():
    my_world = World()
    my_world.add_thing(get_stone(position=None))
    my_world.add_thing(get_grass(position=None))
    my_world.add_thing(get_mirror(position=None))
    my_world.add_agent(get_dummy_agent(position=None))
    my_world.add_agent(get_sheep_agent(position=None))
    my_world.add_agent(get_wolf_agent(position=None))
    my_world.add_agent(get_ape_agent(position=None))
    return my_world


def test_world_create():
    my_world = _setup_world()


def test_world_output():
    my_world = _setup_world()
    my_world.print()
    my_world.map()
    my_world.map(100)


def test_world_run():
    my_world = _setup_world()
    my_world.print()

    for i in range(100):
        my_world.run(time_delta=0.1)

    my_world.print()
