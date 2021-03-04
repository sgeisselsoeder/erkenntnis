from ..behavior_simple_memory import Behavior_simple_memory
from ..world_actions import *
from ..analyze_perception import split_perception_by_type
from ..utils import random_position, vector_length
from .ai_action_interface import action_to_numeric_encoding, numeric_encoding_to_action


class Behavior_monkey_hardcode(Behavior_simple_memory):
    def __init__(self, action_distance: float):
        super().__init__(memory_length=100)
        self.current_target_direction = None
        self.action_distance = action_distance
        self.type_name = "monkey"

    def _hunt(self, prey):
        direction_to_nearest = prey.position

        eating_distance = self.action_distance
        current_distance = vector_length(direction_to_nearest)
        if current_distance < eating_distance:
            action = action_eat(direction=direction_to_nearest)
        else:
            action = action_accelerate(direction=direction_to_nearest)
        cause = prey.unique_properties
        return action, cause

    def _flee(self, enemy):
        direction_to_enemy = enemy.position
        action = action_accelerate(direction=-1.0 * direction_to_enemy)
        cause = enemy.unique_properties
        return action, cause

    def think(self, perception, messages):
        action = None
        cause = None

        for message in messages:
            if message["message"] == "malus":
                action = action_remove_malus()
                cause = message["from"]

        # TODO: react to other messages as well

        # Without messages, we analyze what we see
        split_perception = split_perception_by_type(perception=perception)

        if action is None and self.type_name in split_perception:
            for peer in split_perception[self.type_name]:
                if peer.malus:
                    action = action_inform_malus(direction=peer.position)
                    cause = peer.unique_properties
                    break

        # flee enemies
        for danger in ["wolf"]:
            if action is None and danger in split_perception:
                nearest_enemy = split_perception[danger][0]
                action, cause = self._flee(nearest_enemy)
                break

        # favored prey
        for prey_category in ["sheep"]:
            if action is None and prey_category in split_perception:
                nearest_sheep = split_perception[prey_category][0]
                action, cause = self._hunt(nearest_sheep)
                break

        # talk to peers
        if action is None and self.type_name in split_perception:
            nearest_peer = split_perception[self.type_name][0]
            peer_name = nearest_peer.unique_properties
            if not peer_name in self.last_causes:
                # say hello
                action = action_communicate(direction=nearest_peer.position)
                # action = action_accelerate(direction=nearest_peer.velocity)
            elif self.last_actions[-1]["type"] == "communication" and self.last_causes[-1] == peer_name:
                # travel together
                action = action_point_out(direction=nearest_peer.position,
                                            pointing_direction=0.5 * nearest_peer.velocity -
                                            0.5 * nearest_peer.position,
                                            reason=0.3)
            else:
                action = action_accelerate(direction=nearest_peer.velocity)

            if action is not None:
                cause = nearest_peer.unique_properties


        # backup prey
        for prey_category in ["grass"]:
            if action is None and prey_category in split_perception:
                nearest_sheep = split_perception[prey_category][0]
                action, cause = self._hunt(nearest_sheep)
                break

        if action is None:
            # we might want to keep a direction, but random for now
            if np.random.random() < 0.9:
                self.current_target_direction = random_position()
                action = action_accelerate(
                    direction=self.current_target_direction)
            else:
                action = action_focus()

        self._remember(perception=perception, messages=messages, action=action, cause=cause)
        
        encoded_action = action_to_numeric_encoding(action=action)
        action = numeric_encoding_to_action(encoding=encoded_action)
        return action, cause
