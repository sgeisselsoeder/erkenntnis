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
    return {"type": "inform_malus",
            "direction": direction}


def action_communicate(direction, message: str = "lol"):
    return {"type": "communicate",
            "direction": direction,
            "message": message}


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
    elif action["type"] == "communicate":
        target = action[""]

    elif action["type"] == "interact":
        pass

    else:
        raise("Unrecognized action " + str(action["type"]) + " for agent of type " + str(agent.type_properties))
