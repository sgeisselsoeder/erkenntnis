from .agent import Agent
from .thing import Thing


def perform_action(world, agent: Agent, action, surroundings, time_delta):
    # some actions don't affect other objects (agents, things). The agent can
    if action["type"] == "accelerate":
        agent.accelerate(action["direction"], dt=time_delta)

    elif action["type"] == "interact":
        pass

    else:
        raise("Unrecognized action " + str(action["type"]) + " for agent of type " + str(agent.type_properties))
