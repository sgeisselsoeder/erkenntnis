import numpy as np
from .agent import Agent
from .utils import normalize_vector_3d, random_position, vector_length


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
    number_actions = len(available_actions.keys)
    which_action = int(np.random.random() / (1.0 / number_actions))
    action_type = available_actions.keys[which_action]

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


def _agent_agent_communication(agent, action, surroundings):
    _numeric_location_accuracy = 0.001
    target_position = agent.position + action["direction"]
    for thing in surroundings:
        if np.sum(np.abs(target_position - thing.position)) < _numeric_location_accuracy:
            if isinstance(thing, Agent):
                thing.messages.append({"from": agent.unique_properties,
                                       "from_location": agent.position,
                                       "message": action["message"]})


def _agent_push_agent(agent, action, surroundings):
    # moves a thing away from the agent, but also accelerates the agent in the opposite direction
    # stronger push at higher agent velocity
    _numeric_location_accuracy = 0.001
    _maximal_action_range = agent.max_speed
    if vector_length(action["direction"]) > _maximal_action_range:
        return

    target_position = agent.position + action["direction"]
    normalized_direction = normalize_vector_3d(action["direction"])

    strength = np.minimum(np.fabs(action["strength"]), 1.0) * 0.5
    total_strength = strength * (vector_length(agent.velocity) + 1.0)

    for thing in surroundings:
        if np.sum(np.abs(target_position - thing.position)) < _numeric_location_accuracy:
            # determine how much of the momentum should go to the other agent
            thing.accelerate(direction=normalized_direction, dt=total_strength)
            agent.accelerate(direction=-1.0 * normalized_direction, dt=total_strength)


def _agent_pull_agent(agent, action, surroundings):
    # moves a thing towards the agent, but also accelerates the agent in the opposite direction
    # pull is not affected by agent velocity
    _numeric_location_accuracy = 0.001
    _maximal_action_range = 0.6 * agent.max_speed
    if vector_length(action["direction"]) > _maximal_action_range:
        return

    target_position = agent.position + action["direction"]
    normalized_direction = normalize_vector_3d(action["direction"])

    strength = np.minimum(np.fabs(action["strength"]), 1.0) * 0.25
    total_strength = strength

    for thing in surroundings:
        if np.sum(np.abs(target_position - thing.position)) < _numeric_location_accuracy:
            # determine how much of the momentum should go to the other agent
            thing.accelerate(direction=-1.0 * normalized_direction, dt=total_strength)
            agent.accelerate(direction=normalized_direction, dt=total_strength)


def _agent_attack(agent, action, surroundings):
    # damages a thing. more damage than eat, but also no health restoration possible
    _numeric_location_accuracy = 0.001
    _maximal_action_range = agent.max_speed
    if vector_length(action["direction"]) > _maximal_action_range:
        return

    strength = np.minimum(np.fabs(action["strength"]), 1.0)
    total_strength = strength * agent.strength

    target_position = agent.position + action["direction"]

    for thing in surroundings:
        if np.sum(np.abs(target_position - thing.position)) < _numeric_location_accuracy:
            # determine how much of the momentum should go to the other agent
            thing.health -= total_strength


def _agent_eat(agent, action, surroundings):
    # eats a thing to restore health. Less damage possible than with attack
    _numeric_location_accuracy = 0.001
    _maximal_action_range = agent.max_speed
    if vector_length(action["direction"]) > _maximal_action_range:
        return

    strength = np.minimum(np.fabs(action["strength"]), 1.0)
    total_strength = 0.5 * strength * agent.strength

    target_position = agent.position + action["direction"]
    for thing in surroundings:
        if np.sum(np.abs(target_position - thing.position)) < _numeric_location_accuracy:
            # determine how much of the momentum should go to the other agent
            thing.health -= total_strength
            agent.health += total_strength * 0.5


def perform_action(world, agent: Agent, action, surroundings, time_delta):
    if action["type"] == "accelerate":
        normalized_direction = normalize_vector_3d(action["direction"])
        strength = np.minimum(np.fabs(action["strength"]), 1.0)
        agent.accelerate(normalized_direction, dt=time_delta, strength=strength)

    elif action["type"] == "focus":
        agent.perception_radius = 2.0 * agent.perception_radius
        # this buff will automatically be reset after the next perception by the world

    elif action["type"] == "remove_malus":
        agent.malus = -1
        # removes the malus, but prevents actions for some time
        agent.action_cooldown = 20

    elif action["type"] == "communicate":
        _agent_agent_communication(agent=agent, action=action, surroundings=surroundings)

    elif action["type"] == "point":
        com_action = action_communicate(direction=action["agent_direction"],
                                        message={"pointing_direction": action["pointing_direction"],
                                                 "reason": action["reason"]})
        _agent_agent_communication(agent=agent, action=com_action, surroundings=surroundings)

    elif action["type"] == "push":
        _agent_push_agent(agent=agent, action=action, surroundings=surroundings)

    elif action["type"] == "pull":
        _agent_pull_agent(agent=agent, action=action, surroundings=surroundings)

    elif action["type"] == "attack":
        _agent_attack(agent=agent, action=action, surroundings=surroundings)
        # agent.action_cooldown = 5

    elif action["type"] == "eat":
        _agent_eat(agent=agent, action=action, surroundings=surroundings)
        # agent.action_cooldown = 3

    elif action["type"] == "inform_malus":
        _agent_agent_communication(agent=agent, action=action, surroundings=surroundings)

    else:
        raise("Unrecognized action " + str(action["type"]) + " for agent of type " +
              str(type(agent)) + " " + str(agent.type_properties))
