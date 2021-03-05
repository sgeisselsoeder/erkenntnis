from erkenntnis.brain_implementation.ai_action_interface import *
from erkenntnis.world_actions import *
from erkenntnis.utils import random_position


available_test_actions = {"accelerate": ["direction1", "direction2", "strength"],
                          "focus": None,
                          "remove_malus": None,
                          "communicate": ["direction1", "direction2", "message"],
                          "point": ["direction1", "direction2", "point_direction1", "point_direction2", "reason"],
                          "push": ["direction1", "direction2", "strength"],
                          "pull": ["direction1", "direction2", "strength"],
                          "attack": ["direction1", "direction2", "strength"],
                          "eat": ["direction1", "direction2", "strength"],
                          "inform_malus": ["direction1", "direction2"]}
# 0 "accelerate": [
# 1 "direction1",
# 2 "direction2",
# 3 "strength"],
#
# 4 "focus": None,
#
# 5 "remove_malus": None,
#
# 6 "communicate": [
# 7 "direction1",
# 8 "direction2",
# 9 "message"],
#
# 10 "point": [
# 11 "direction1",
# 12 "direction2",
# 13 "point_direction1",
# 14 "point_direction2",
# 15 "reason"],
#
# 16 "push": [
# 17 "direction1",
# 18 "direction2",
# 19 "strength"],
#
# 20 "pull": [
# 21 "direction1",
# 22 "direction2",
# 23 "strength"],
#
# 24 "attack": [
# 25 "direction1",
# 26 "direction2",
# 27 "strength"],
#
# 28 "eat": [
# 29 "direction1",
# 30 "direction2",
# 31 "strength"],
#
# 32 "inform_malus":
# 33 ["direction1",
# 34 "direction2"],}


def test_available_actions_to_encoding():
    encoding, _ = get_numeric_encoding_and_action_indices(available_actions=available_test_actions)
    assert(encoding.shape[0] == 35)


def test_action_encoding_action_conversions():
    action = action_accelerate(direction=random_position(), strength=0.6)
    encoded = action_to_numeric_encoding(action=action, available_actions=available_test_actions)
    action2 = numeric_encoding_to_action(encoding=encoded, available_actions=available_test_actions)
    for key in action:
        assert(np.all(action[key] == action2[key]))

    # action = action_point_out(agent_direction=random_position(), pointing_direction=random_position(), reason=0.88)
    # encoded = action_to_numeric_encoding(action=action)
    # action2 = numeric_encoding_to_action(encoding=encoded)
    # assert(action == action2)

    action = action_point_out(agent_direction=random_position(), pointing_direction=random_position(), reason=0.88)
    encoded = action_to_numeric_encoding(action=action, available_actions=available_test_actions)
    action2 = numeric_encoding_to_action(encoding=encoded, available_actions=available_test_actions)
    for key in action:
        assert(np.all(action[key] == action2[key]))


def test_encoding_action_encoding_conversions():
    encoded, _ = get_numeric_encoding_and_action_indices(available_actions=available_test_actions)
    encoded[4] = 1.0    # focus
    action = numeric_encoding_to_action(encoding=encoded, available_actions=available_test_actions)
    encoded2 = action_to_numeric_encoding(action=action, available_actions=available_test_actions)
    assert(np.all(encoded == encoded2))

    encoded, _ = get_numeric_encoding_and_action_indices(available_actions=available_test_actions)
    encoded[5] = 1.0    # remove malus
    action = numeric_encoding_to_action(encoding=encoded, available_actions=available_test_actions)
    encoded2 = action_to_numeric_encoding(action=action, available_actions=available_test_actions)
    assert(np.all(encoded == encoded2))

    encoded, _ = get_numeric_encoding_and_action_indices(available_actions=available_test_actions)
    encoded[16] = 1.0   # push
    encoded[17] = 0.7
    encoded[18] = 0.57
    encoded[19] = 0.1
    action = numeric_encoding_to_action(encoding=encoded, available_actions=available_test_actions)
    encoded2 = action_to_numeric_encoding(action=action, available_actions=available_test_actions)
    assert(np.all(encoded == encoded2))


def test_action_encoding_conversions():
    action = action_accelerate(direction=random_position(), strength=0.6)
    offset = 0
    encoded = action_to_numeric_encoding(action, available_actions=available_test_actions)
    assert(encoded[offset + 0] == 1.0)
    assert(encoded[offset + 1] == action["direction"][0])
    assert(encoded[offset + 2] == action["direction"][1])
    assert(encoded[offset + 3] == action["strength"])

    action = action_attack(direction=random_position(), strength=0.4)
    offset = 24
    encoded = action_to_numeric_encoding(action, available_actions=available_test_actions)
    assert(encoded[offset + 0] == 1.0)
    assert(encoded[offset + 1] == action["direction"][0])
    assert(encoded[offset + 2] == action["direction"][1])
    assert(encoded[offset + 3] == action["strength"])

    action = action_eat(direction=random_position(), strength=0.2)
    offset = 28
    encoded = action_to_numeric_encoding(action, available_actions=available_test_actions)
    assert(encoded[offset + 0] == 1.0)
    assert(encoded[offset + 1] == action["direction"][0])
    assert(encoded[offset + 2] == action["direction"][1])
    assert(encoded[offset + 3] == action["strength"])

    action = action_communicate(direction=random_position(), message="lol_test")
    encoded = action_to_numeric_encoding(action, available_actions=available_test_actions)
    offset = 6  # communicate, --> 7 - 1
    assert(encoded[offset + 0] == 1.0)
    assert(encoded[offset + 1] == action["direction"][0])
    assert(encoded[offset + 2] == action["direction"][1])
    # assert(encoded[offset + 3] == action["message"])
    assert(encoded[offset + 3] == 0.5)

    action = action_communicate(direction=random_position(), message=0.57)
    encoded = action_to_numeric_encoding(action, available_actions=available_test_actions)
    offset = 6  # communicate, --> 7 - 1
    assert(encoded[offset + 0] == 1.0)
    assert(encoded[offset + 1] == action["direction"][0])
    assert(encoded[offset + 2] == action["direction"][1])
    assert(encoded[offset + 3] == action["message"])

    action = action_inform_malus(direction=random_position())
    encoded = action_to_numeric_encoding(action, available_actions=available_test_actions)
    offset = 32
    assert(encoded[offset + 0] == 1.0)
    assert(encoded[offset + 1] == action["direction"][0])
    assert(encoded[offset + 2] == action["direction"][1])
