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
    def __init__(self, world_scale: float = 100.0):
        self.world_scale = world_scale
        self.time = 0
        self.agents = list()
        self.things = list()

    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    def add_thing(self, thing: Thing):
        self.things.append(thing)

    def add(self, thing: Thing, position: np.ndarray = None):
        if position is not None:
            thing.position = position
        if isinstance(thing, Agent):
            self.add_agent(thing)
        else:
            self.add_thing(thing)

    def process_agent(self, agent: Agent, time_delta=0.01):
        perception, raw_perception = perception_at_position(all_things=self.things + self.agents,
                                                            position=agent.position,
                                                            radius=agent.perception_radius)
        agent.perception_radius = agent.default_perception_radius

        if agent.action_cooldown <= 0:
            action = agent.think(perception=perception)
            # NOTE: unclear if it's better to execute the action for each agent immediatelly
            # or to store them and execute all actions at once.
            #
            # pro for immediatelly: - easiest to code
            #                       - other agents will be able to react to the first agent (maybe mitigating the drawback of acting later),
            #                       - no conflicting actions possible (but unrealistic first come (in array), first serve)
            # pro for later:    - feels more realistic,
            #                   - potentially possible to resolve conflicting actions if they are all known at the same time
            #
            # current solution: immediate action: easier to resolve conflicts, "unrealistic" order should not be relevant for current goal
            if action is not None:
                perform_action(world=self, agent=agent, action=action, surroundings=raw_perception, time_delta=time_delta)
        else:
            agent.action_cooldown = agent.action_cooldown - 1

        # agents struggle to survive
        agent.health -= 0.2

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
            if agent.health >= 200:
                agent.health = 110
                new_agent = copy.deepcopy(agent)
                new_agent.position = agent.position + random_position()
                new_agent.unique_properties = uuid.uuid1()
                self.agents.append(new_agent)

    def _malus_effect(self):
        for current_agent in self.agents:
            # check agent malus state
            if current_agent.malus > 0:     # having malus, but time left
                current_agent.malus -= 1

            elif current_agent.malus == 0:  # having malus, time to die
                current_agent.health = -1

            else:                           # malus free, but could randomly get it
                new_malus_probability = 0.0
                # new_malus_probability = 0.01
                if np.random.random() <= new_malus_probability:
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
        print_map(get_map(self.things + self.agents, size=resolution, fixed_boundary=fixed_boundary), plotstyle=plotstyle)

    def save(self, filename: str = None):
        if filename is None:
            filename = "world_" + str(self.time) + "_a" + str(len(self.agents)) + "_t" + str(len(self.things)) + ".pkl"
        with open(filename, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        return filename
