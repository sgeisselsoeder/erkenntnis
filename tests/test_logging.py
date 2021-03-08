from erkenntnis.world import *


def test_logging_loadable():
    my_world = World(agent_health_decline=0.0, malus_propability=0.0)

    my_world.add(new_dummy_agent(), position=np.array([0.0, 0.0, 0.0]))

    number_time_steps = 9
    for i in range(number_time_steps):
        my_world.run(time_delta=0.1)

    agent = my_world.agents[0]
    logfilename = agent.brain.logfile

    logdata = np.loadtxt(logfilename)


def test_logging_correct_values():
    my_world = World(agent_health_decline=0.0, malus_propability=0.0)

    position_1 = 0.456123
    position_2 = 0.789321
    my_world.add(new_stone(), position=np.array([position_1, position_2, 0.0]))
    my_world.add(new_dummy_agent(), position=np.array([0.0, 0.0, 0.0]))

    number_time_steps = 9
    for i in range(number_time_steps):
        my_world.run(time_delta=0.1)

    agent = my_world.agents[0]
    logfilename = agent.brain.logfile

    logdata = np.loadtxt(logfilename)
    assert(logdata.shape[0] == number_time_steps)
    positions = [position_1, position_2]
    assert(np.sum(np.isin(element=logdata[0], test_elements=positions)) == len(positions))
