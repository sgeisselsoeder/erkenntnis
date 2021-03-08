from erkenntnis.world import *


def test_sheep_eats_gras():
    my_world = World(agent_health_decline=0.0, malus_propability=0.0)

    my_world.add(new_grass(), position=np.array([1.0, 0.0, 0.0]))
    my_world.add(new_sheep(), position=np.array([1.0, 1.0, 0.0]))
    for i in range(10):
        my_world.run(time_delta=0.1)

    assert(len(my_world.things) == 0)
    assert(len(my_world.agents) == 1)
    assert(my_world.agents[0].type_properties == "sheep")
    assert(my_world.agents[0].health > 80.0)


def test_wolf_eats_sheep():
    my_world = World(agent_health_decline=0.0, malus_propability=0.0)

    my_world.add(new_sheep(), position=np.array([1.0, 0.0, 0.0]))
    my_world.add(new_wolf(), position=np.array([2.0, 2.0, 0.0]))
    for i in range(100):
        my_world.run(time_delta=0.1)

    assert(len(my_world.things) == 0)
    assert(len(my_world.agents) == 1)
    assert(my_world.agents[0].type_properties == "wolf")
    assert(my_world.agents[0].health >= 140.0)


def test_sheep_has_kid():
    initial_world_scale = 2

    my_world = World(world_scale=initial_world_scale, agent_health_decline=0.0, malus_propability=0.0)

    number_gras = 25
    for i in range(number_gras):
        my_world.add(new_grass(), position=random_position(scale=initial_world_scale))
    my_world.add(new_sheep(), position=np.array([1.0, 0.0, 0.0]))

    for i in range(200):
        my_world.run(time_delta=0.1)

    assert(len(my_world.things) < number_gras)
    assert(len(my_world.agents) > 1)
