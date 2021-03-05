from erkenntnis.world import *


def test_monkey_attack_sheep():
    my_world = World(agent_health_decline=0.0, malus_propability=0.0)

    my_world.add(new_sheep(health=10.0), position=np.array([0.0, 0.0, 0.0]))
    my_world.add(new_monkey(), position=np.array([1.0, 0.0, 0.0]))
    for i in range(10):
        my_world.run(time_delta=0.1)

    assert(len(my_world.things) == 0)
    assert(len(my_world.agents) == 1)
    assert(my_world.agents[0].type_properties == "monkey")
    assert(my_world.agents[0].health > my_world.agents[0].default_health)


def test_monkey_flees_wolf():
    my_world = World(agent_health_decline=0.0, malus_propability=0.0)

    my_world.add(new_monkey(), position=np.array([7.0, 0.0, 0.0]))
    my_world.add(new_wolf(), position=np.array([0.0, 0.0, 0.0]))
    for i in range(100):
        my_world.run(time_delta=0.1)

    assert(len(my_world.things) == 0)
    assert(len(my_world.agents) == 2)
    assert(my_world.agents[0].health == my_world.agents[0].default_health)
    assert(my_world.agents[1].health == my_world.agents[1].default_health)


def test_monkies_fixing_malus():
    my_world = World(agent_health_decline=0.0, malus_propability=0.0)

    my_world.add(new_monkey(), position=np.array([2.0, 0.0, 0.0]))
    my_world.add(new_monkey(), position=np.array([0.0, 0.0, 0.0]))
    my_world.agents[0].malus = 10

    for i in range(5):
        my_world.run(time_delta=0.1)

    assert(len(my_world.agents) == 2)
    for agent in my_world.agents:
        assert(agent.malus == -1)


def test_monkey_talks_to_monkey():
    my_world = World(agent_health_decline=0.0, malus_propability=0.0)

    my_world.add(new_monkey(), position=np.array([2.0, 0.0, 0.0]))
    my_world.add(new_monkey(), position=np.array([0.0, 0.0, 0.0]))

    for i in range(5):
        my_world.run(time_delta=0.1)

    communication_found = False
    for i in range(5):
        if my_world.agents[0].brain.last_actions[-i]["type"] == "communicate":
            if my_world.agents[0].brain.last_causes[-i] == my_world.agents[1].unique_properties:
                communication_found = True
    assert(communication_found)
