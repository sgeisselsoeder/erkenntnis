import numpy as np
import copy
import uuid
import pickle

from .thing import Thing
from .agent import Agent
from .world_perception import perception_at_position
from .world_creation import *
from .world_map import get_map, print_map
from .world_actions import perform_action
from .utils import random_position


def load_world(filename: str):
    with open(filename, 'rb') as input:
        world = pickle.load(input)
    return world


class World:
    def __init__(self, world_scale: float = 100.0, agent_health_decline: float = 0.3, malus_propability: float = 0.01):
        self.world_scale = world_scale
        self.time = 0
        self.agents = list()
        self.things = list()
        self.agent_health_decline = agent_health_decline
        self.malus_propability = malus_propability
        self.thing_enumerator = 1

    def add_agent(self, agent: Agent):
        agent.unique_properties = self.thing_enumerator
        self.thing_enumerator += 1
        self.agents.append(agent)

    def add_thing(self, thing: Thing):
        thing.unique_properties = self.thing_enumerator
        self.thing_enumerator += 1
        self.things.append(thing)

    def add(self, thing: Thing, position: np.ndarray = None):
        if position is not None:
            thing.position = position
        if isinstance(thing, Agent):
            self.add_agent(thing)
        else:
            self.add_thing(thing)

    # NOTE: unclear if it's better to execute the action for each agent immediatelly
    # or to store them and execute all actions at once.
    #
    # pro for immediatelly: - easiest to code
    #                       - other agents will be able to react to the first agent
    #                           (maybe mitigating the drawback of acting later),
    #                       - no conflicting actions possible (but unrealistic first come (in array), first serve)
    # pro for later:    - feels more realistic,
    #                   - potentially possible to resolve conflicting actions if they are all known at the same time
    #
    # current solution: immediate action: easier to resolve conflicts, "unrealistic" order
    #                   should not be relevant for current goals
    def process_agent(self, agent: Agent, time_delta=0.01):
        perception, raw_perception = perception_at_position(all_things=self.things + self.agents,
                                                            position=agent.position,
                                                            radius=agent.perception_radius,
                                                            max_things=agent.max_number_perceived_things)

        # reset the perception radius of the agent to clear increased radius from focus action
        agent.perception_radius = agent.default_perception_radius

        old_cooldown = agent.action_cooldown
        action = agent.think(perception=perception)

        if old_cooldown > 0:
            if agent.action_cooldown != old_cooldown - 1:
                print("NO CHEATING! AGENTS MUST RESPECT THEIR COOLDOWN")
                agent.action_cooldown = old_cooldown - 1

            if action is not None:
                print("NO CHEATING! NO AGENT ACTIONS DURING COOLDOWN")
                action = None

        if action is not None:
            perform_action(world=self, agent=agent, action=action, surroundings=raw_perception, time_delta=time_delta)

        # agents struggle to survive
        agent.health -= self.agent_health_decline * time_delta

    def _remove_dead(self):
        things_to_remove = list()
        for current_thing in self.things + self.agents:
            if current_thing.health <= 0:
                things_to_remove.append(current_thing)

        for thing in things_to_remove:
            try:
                self.agents.remove(thing)
            except ValueError:
                try:
                    self.things.remove(thing)
                except ValueError:
                    raise "Unable to find " + str(thing) + " with health " + str(thing.health) + " in world."

    def _spawn_kids(self):
        for agent in self.agents:
            if agent.health >= 2.0 * agent.default_health:
                agent.health = 0.5 * agent.health
                new_agent = copy.deepcopy(agent)
                new_agent.position = agent.position + random_position()
                new_agent.unique_properties = self.thing_enumerator
                self.thing_enumerator += 1
                if agent.brain.logfile is not None:
                    new_agent.brain.logfile = agent.brain.logfile + "_" + str(new_agent.unique_properties) + ".npy"
                self.agents.append(new_agent)

    def _malus_effect(self):
        for current_agent in self.agents:
            # check agent malus state
            if current_agent.malus > 0:     # having malus, but time left
                current_agent.malus -= 1

            elif current_agent.malus == 0:  # having malus, time to die
                current_agent.health = -1

            else:                           # malus free, but could randomly get it
                if np.random.random() <= self.malus_propability:
                    current_agent.malus = 30

    def run(self, time_delta=0.01):
        # TODO for fairer simulation, either random order or according to agent initiative, ... ?
        for agent in self.agents:
            self.process_agent(agent, time_delta=time_delta)

        for current_thing in self.things + self.agents:
            current_thing.move(dt=time_delta)

        self._malus_effect()
        self._remove_dead()
        self._spawn_kids()

        self.time = self.time + time_delta

    def print(self):
        print("Time is ", self.time)
        for this_thing in self.things + self.agents:
            print(this_thing)

    def map(self, resolution: int = 40, fixed_boundary: float = None, plotstyle: str = "sparse"):
        print_map(get_map(self.things + self.agents, size=resolution,
                          fixed_boundary=fixed_boundary), plotstyle=plotstyle)

    def save(self, filename: str = None):
        if filename is None:
            filename = "world_" + str(self.time) + "_a" + str(len(self.agents)) + "_t" + str(len(self.things)) + ".pkl"
        with open(filename, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        return filename
