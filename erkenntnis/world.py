from .agent import agent


class world:
    agents = list()

    def add_agent(self):
        self.agents.append(agent())
