from .agent import Agent
from .thing import Thing

_allowed_actions = {"dummy": ["accelerate", "focus"]}


# def action_talk(self, agent, message):

# def action_notify(self, agent, direction):
#     # alternatively also target agent

# def action_interact(self, direction):

# def action_attack(self, direction):


def perform_action(world, agent: Agent, action, surroundings, time_delta):
    # some actions don't affect other objects (agents, things). The agent can
    if action["type"] == "accelerate":
        agent.accelerate(action["direction"], dt=time_delta)
    elif action["type"] == "focus":
        agent.perception_radius = 2.0 * agent.perception_radius
        # this buff will be reset after the next perception by the world
    elif action["type"] == "remove_malus":
        agent.malus = False
        # removes the malus, but prevents actions for some time
        agent.action_cooldown = 50


    elif action["type"] == "interact":
        pass

    else:
        raise("Unrecognized action " + str(action["type"]) + " for agent of type " + str(agent.type_properties))
