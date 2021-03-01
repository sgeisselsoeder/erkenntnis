import numpy as np
from .agent import Agent
from .thing import Thing


def action_accelerate(direction, strength=1.0):
    return {"type": "accelerate",
            "direction": direction,
            "strength": strength}


def action_focus():
    return {"type": "focus"}


def action_remove_malus():
    return {"type": "remove_malus"}


def action_inform_malus(direction):
    return action_communicate(direction=direction, message="malus")


def action_communicate(direction, message: str = "lol"):
    return {"type": "communicate",
            "direction": direction,
            "message": message}


def action_point_in_direction(agent_direction, pointing_direction, reason: str = "WorthyGoal"):
    return {"type": "point",
            "agent_direction": agent_direction,
            "pointing_direction": pointing_direction,
            "reason": reason}


def action_attack(direction, strength=1.0):
    return {"type": "attack",
            "direction": direction,
            "strength": strength}


def action_push(direction, strength=1.0):
    return {"type": "push",
            "direction": direction,
            "strength": strength}


def action_pull(direction, strength=1.0):
    return {"type": "pull",
            "direction": direction,
            "strength": strength}


# _allowed_actions = {"dummy": ["accelerate", "focus"]}


def _agent_com(agent, action, surroundings):
    _numeric_location_accuracy = 0.001
    target_position = agent.position + action["direction"]
    for thing in surroundings:
        if np.sum(np.abs(target_position - thing.position)) < _numeric_location_accuracy:
            if isinstance(thing, Agent):
                thing.messages.append({"from": agent.unique_properties,
                                       "from_location": agent.position,
                                       "message": action["message"]})


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
        agent.action_cooldown = 20
    elif action["type"] == "communicate":       # this also covers inform_malus
        _agent_com(agent=agent, action=action, surroundings=surroundings)
    else:
        raise("Unrecognized action " + str(action["type"]) + " for agent of type " +
              str(type(agent)) + " " + str(agent.type_properties))
