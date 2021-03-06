from ..brain_simple_memory import Brain_simple_memory
from ...world_actions import *
from .world_model import Worldmodel
from ..ai_action_interface import _available_actions


class Brain_ape_ml(Brain_simple_memory):
    def __init__(self, action_distance: float):
        super().__init__(memory_length=100)
        self.current_target_direction = None
        self.action_distance = action_distance
        self.world_model = Worldmodel()
        self.behavior = None

    def _predict_one_action(self, encoded_perception, encoded_messages, action):
        self.world_model.estimate_future_state(encoded_perception, encoded_messages, last_states=self.last_perceptions,
                                               last_actions=self.last_actions, next_action=action)

    def predict_best_action(self, encoded_perception, encoded_messages):
        best_score = 0.0
        best_action = None
        for action in _available_actions:
            prediction = self._predict_one_action(encoded_perception, encoded_messages, action)
            score = self.score_prediction(prediction)
            if score > best_score:
                best_score = score
                best_action = action
        return best_action

    def think(self, encoded_perception, encoded_messages):

        action = None
        cause = None

        current_state = self.world_model.comprehend_state(encoded_perception=encoded_perception, encoded_messages=encoded_messages)

        action = self.predict_best_action(encoded_perception=encoded_perception, encoded_messages=encoded_messages)

        self._remember(perception=encoded_perception, messages=encoded_messages, action=action, cause=None)
        return action
