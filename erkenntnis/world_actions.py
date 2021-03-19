import numpy as np
from .agent import Agent
from .utils import normalize_vector_3d, vector_length
from .available_actions import *


def _agent_agent_communication(agent, action, surroundings):
    _numeric_location_accuracy = 0.001
    target_position = agent.position + action["direction"]
    for thing in surroundings:
        if np.sum(np.abs(target_position - thing.position)) < _numeric_location_accuracy:
            # if isinstance(thing, Agent):
            try:
                thing.messages.append({"from": agent.unique_properties,
                                       "from_location": agent.position,
                                       "message": action["message"]})
            except Exception:
                pass    # things don't have message lists, agents do


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
        # also wounds the agent severely
        agent.health = 0.3 * agent.health

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
