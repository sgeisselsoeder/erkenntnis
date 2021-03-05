from .thing import Thing
from .brain_implementation.brain import Brain
from .brain_implementation.ai_action_interface import numeric_encoding_to_action
from .brain_implementation.ai_perception_interface import encode_perception


class Agent(Thing):
    def __init__(self, brain: Brain, position, velocity=None, radius=None, default_health: float = None,
                 health: float = None, strength: float = 10.0, perception_radius=None, max_speed: float = 3.0,
                 max_number_perceived_things: int = 0):
        super().__init__(position=position, velocity=velocity, radius=radius, health=health, default_health=default_health,
                         max_speed=max_speed, strength=strength)

        self.brain = brain
        self.action_cooldown = 0

        self.default_perception_radius = 10.0
        if perception_radius is not None:
            self.default_perception_radius = perception_radius
        self.perception_radius = self.default_perception_radius

        self.max_number_perceived_things = max_number_perceived_things

        # option to store received messages from other agents.
        # should be emptied by the world upon perceive() or by themselves at the beginning of think
        self.messages = list()

        self.last_action = None
        self.last_cause = None

        # could be equivalent to encoding of size of sheep, fur of wolf, number of limbs, ...
        self.type_properties = "agent"

    def think(self, perception):
        # if len(perception) > 0:
        #     encoded_perception = encode_perception(perception[:1], expected_number_perceptions=self.max_number_perceived_things)
        encoded_action, cause = self.brain.think(perception=perception, messages=self.messages)
        action = numeric_encoding_to_action(encoding=encoded_action)
        self.last_action = action
        self.last_cause = cause
        self.messages.clear()
        return action
