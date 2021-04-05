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

    position_1 = 0.4561
    position_2 = 0.7894
    my_world.add(new_stone(), position=np.array([position_1, position_2, 0.0]))
    # my_world.add(new_dummy_agent(), position=np.array([0.0, 0.0, 0.0]))
    my_world.add(new_monkey(log=True), position=np.array([0.0, 0.0, 0.0]))

    number_time_steps = 9
    for i in range(number_time_steps):
        my_world.run(time_delta=0.1)

    agent = my_world.agents[0]
    logfilename = agent.brain.logfile

    logdata = np.loadtxt(logfilename)
    # the assert can fail if remove_malus action was performed.
    # this action then has a cooldown and hence no thinking will happen and also no logging.
    # therefore the shape of the logged data can be smaller ...
    # TODO: fix, also logging without thinking.
    assert(logdata.shape[0] == number_time_steps)

    entry = np.around(position_1, decimals=3)
    found = False
    for number in logdata[0]:
        if np.around(number, decimals=3) == entry:
            found = True
            break
    assert(found)

    entry = np.around(position_2, decimals=3)
    found = False
    for number in logdata[0]:
        if np.around(number, decimals=3) == entry:
            found = True
            break
    assert(found)
