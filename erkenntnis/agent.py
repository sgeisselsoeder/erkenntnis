from .thing import Thing
from .behavior_agent import Behavior


class Agent(Thing):
    def __init__(self, behavior: Behavior, position, velocity=None, radius=None, default_health: float = None,
                 health: float = None, strength: float = 10.0, perception_radius=None, max_speed: float = 3.0):
        super().__init__(position=position, velocity=velocity, radius=radius, health=health, default_health=default_health,
                         max_speed=max_speed, strength=strength)

        self.behavior = behavior
        self.action_cooldown = 0

        self.default_perception_radius = 10.0
        if perception_radius is not None:
            self.default_perception_radius = perception_radius
        self.perception_radius = self.default_perception_radius

        # option to store received messages from other agents.
        # should be emptied by the world upon perceive() or by themselves at the beginning of think
        self.messages = list()

        self.last_action = None
        self.last_cause = None

        # could be equivalent to encoding of size of sheep, fur of wolf, number of limbs, ...
        self.type_properties = "agent"

    def think(self, perception):
        action, cause = self.behavior.think(perception=perception, messages=self.messages)
        self.last_action = action
        self.last_cause = cause
        self.messages.clear()
        return action
