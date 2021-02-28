import numpy as np
from .thing import thing
from .agent import agent
from .world_perception import perception_at_position
# from .world_actions import perform_action


class world:
    time = 0
    agents = list()
    things = list()

    def add_agent(self):
        self.agents.append(agent(position=[np.random(), np.random(), 0.0]))

    def add_thing(self):
        self.things.append(thing(position=[np.random(), np.random(), 0.0]))

    def perception_at_position(self, position, radius):
        all_things = self.things + self.agents
        perception, raw_perception = perception_at_position(all_things=all_things, position=position, radius=radius)
        return perception, raw_perception

    def perform_action(self, agent, action, surroundings, time_delta):
        pass

    def process_agent(self, agent, time_delta=0.01):
        position = agent.position
        perception, raw_perception = self.perception_at_position(position=position, radius=agent.perception_radius)
        action = agent.behavior.think(perception=perception)
        # NOTE: unclear if it's better to execute the action for each agent immediatelly or to store them and execute all actions at once.
        # pro for immediatelly: - easiest to code
        #                       - other agents will be able to react to the first agent (maybe mitigating the drawback of acting later),
        #                       - no conflicting actions possible (but unrealistic first come (in array), first serve)
        # pro for later:    - feels more realistic,
        #                   - potentially possible to resolve conflicting actions if they are all known at the same time
        # current solution: immediate action: easier to resolve conflicts, "unrealistic" order should not be relevant for current goal
        self.perform_action(agent=agent, action=action, surroundings=raw_perception, time_delta=time_delta)
        return 0

    def run(self, time_delta=0.01):
        # TODO for fairer simulation, either random order or according to agent initiative, ... ?
        for agent in self.agents:
            self.process_agent(agent, time_delta=time_delta)

    def print(self):
        print("Time is ", self.time)
        for this_thing in self.things:
            print(this_thing)
        for this_thing in self.agents:
            print(this_thing)
