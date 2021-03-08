import numpy as np
from .utils import random_position


_full_available_actions = {"accelerate": ["direction1", "direction2", "strength"],
                           "focus": None,
                           "remove_malus": None,
                           "communicate": ["direction1", "direction2", "message"],
                           "point": ["direction1", "direction2", "point_direction1", "point_direction2", "reason"],
                           "push": ["direction1", "direction2", "strength"],
                           "pull": ["direction1", "direction2", "strength"],
                           "attack": ["direction1", "direction2", "strength"],
                           "eat": ["direction1", "direction2", "strength"],
                           "inform_malus": ["direction1", "direction2"]}

_limited_actions = {"accelerate": ["direction1", "direction2", "strength"],
                    "focus": None,
                    "remove_malus": None,
                    "communicate": ["direction1", "direction2", "message"],
                    "eat": ["direction1", "direction2", "strength"],
                    "inform_malus": ["direction1", "direction2"]}

_available_actions = _limited_actions


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
            "direction": direction,
            "message": "malus"}
    # return action_communicate(direction=direction, message="malus")


def action_communicate(direction, message=0.5):
    return {"type": "communicate",
            "direction": direction,
            "message": message}


def action_point_out(agent_direction, pointing_direction, reason=0.5):
    return {"type": "point",
            "agent_direction": agent_direction,
            "pointing_direction": pointing_direction,
            "reason": reason}


def action_push(direction, strength=1.0):
    return {"type": "push",
            "direction": direction,
            "strength": strength}


def action_pull(direction, strength=1.0):
    return {"type": "pull",
            "direction": direction,
            "strength": strength}


def action_attack(direction, strength=1.0):
    return {"type": "attack",
            "direction": direction,
            "strength": strength}


def action_eat(direction, strength=1.0):
    return {"type": "eat",
            "direction": direction,
            "strength": strength}


def random_action(available_actions=_available_actions):
    number_actions = len(list(available_actions.keys()))
    which_action = int(np.random.random() / (1.0 / number_actions))
    action_type = list(available_actions.keys())[which_action]

    if action_type == "accelerate":
        return {"type": "accelerate",
                "direction": random_position(),
                "strength": np.random.random()}

    elif action_type == "focus":
        return {"type": "focus"}

    elif action_type == "remove_malus":
        return {"type": "remove_malus"}

    elif action_type == "inform_malus":
        return {"type": "inform_malus",
                "direction": random_position(),
                "message": "malus"}

    elif action_type == "communicate":
        return {"type": "communicate",
                "direction": random_position(),
                "message": np.random.random()}

    elif action_type == "point":
        return {"type": "point",
                "agent_direction": random_position(),
                "pointing_direction": random_position(),
                "reason": np.random.random()}

    elif action_type == "push":
        return {"type": "push",
                "direction": random_position(),
                "strength": np.random.random()}

    elif action_type == "pull":
        return {"type": "pull",
                "direction": random_position(),
                "strength": np.random.random()}

    elif action_type == "attack":
        return {"type": "attack",
                "direction": random_position(),
                "strength": np.random.random()}

    elif action_type == "eat":
        return {"type": "eat",
                "direction": random_position(),
                "strength": np.random.random()}

    else:   # accelerate by default
        return {"type": "accelerate",
                "direction": random_position(),
                "strength": np.random.random()}

# _allowed_actions = {"dummy": ["accelerate", "focus"]}
