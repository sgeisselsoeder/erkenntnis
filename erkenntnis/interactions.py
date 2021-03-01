import numpy as np
from .thing import Thing
from .agent import Agent
from .world_perception import perception_at_position

# below are possibly allowed actions
def action_talk(self, agent, message):
    pass

def action_notify(self, agent, direction):
    # alternatively also target agent
    pass

def action_accelerate(self, direction, strength):
    return None

def action_interact(self, direction):
    return None

def action_attack(self, direction):
    return None

def action_benefit(self, direction):
    return None

def action_benefit_self(self):
    return None

def action_focus(self, direction):
    # gain in depth perception
    return None


class World:
    def __init__(self):
        self.time = 0
        self.agents = list()
        self.things = list()

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_thing(self, thing):
        self.things.append(thing)

    def perception_at_position(self, position, radius):
        all_things = self.things + self.agents
        perception, raw_perception = perception_at_position(all_things=all_things, position=position, radius=radius)
        return perception, raw_perception

    def perform_new_action(self, agent: Agent, action, surroundings, time_delta):
        # some actions don't affect other objects (agents, things). The agent can 
        if action["type"] == "accelerate":
            agent.accelerate(action["direction"], dt=time_delta)

        elif action["type"] == "interact":
            pass

        else:
            raise("Unrecognized action " + str(action["type"]) + " for agent of type " + str(agent.type_properties))

        

    def process_agent(self, agent: Agent, time_delta=0.01):
        perception, raw_perception = self.perception_at_position(position=agent.position, radius=agent.perception_radius)
        action = agent.think(perception=perception)
        # NOTE: unclear if it's better to execute the action for each agent immediatelly or to store them and execute all actions at once.
        # pro for immediatelly: - easiest to code
        #                       - other agents will be able to react to the first agent (maybe mitigating the drawback of acting later),
        #                       - no conflicting actions possible (but unrealistic first come (in array), first serve)
        # pro for later:    - feels more realistic,
        #                   - potentially possible to resolve conflicting actions if they are all known at the same time
        # current solution: immediate action: easier to resolve conflicts, "unrealistic" order should not be relevant for current goal
        self.perform_new_action(agent=agent, action=action, surroundings=raw_perception, time_delta=time_delta)

        # every object can also move according to it's already gained momentum
        agent.move(dt=time_delta)
        return 0

    def run(self, time_delta=0.01):
        # print("Time ", self.time)
        # TODO for fairer simulation, either random order or according to agent initiative, ... ?
        for agent in self.agents:
            self.process_agent(agent, time_delta=time_delta)

        for current_thing in self.things:
            current_thing.move(dt=time_delta)

        self.time = self.time + time_delta

    def print(self):
        print("Time is ", self.time)
        for this_thing in self.things:
            print(this_thing)
        for this_thing in self.agents:
            print(this_thing)

    def map(self, size: int = 40):
        all_things = self.things + self.agents
        map = get_map(all_things, size=size)
        print_map(map)
