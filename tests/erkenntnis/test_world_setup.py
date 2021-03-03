from erkenntnis.world import *
from tests.erkenntnis.test_thing_and_agent_creation import _get_new_thing_type


def _setup_world():
    my_world = World()
    my_world.add_thing(new_stone(position=None))
    my_world.add_thing(new_grass(position=None))
    my_world.add_thing(new_mirror(position=None))
    my_world.add_agent(new_dummy_agent(position=None))
    my_world.add_agent(new_sheep(position=None))
    my_world.add_agent(new_wolf(position=None))
    my_world.add_agent(new_ape(position=None))
    return my_world


def test_world_create():
    my_world = _setup_world()
    assert(my_world is not None)


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


def test_world_with_new_item():
    my_world = _setup_world()
    thing = _get_new_thing_type()
    my_world.add(thing)
    my_world.print()

    for i in range(100):
        my_world.run(time_delta=0.1)

    my_world.print()
