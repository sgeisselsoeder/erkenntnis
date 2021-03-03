from erkenntnis.behavior_implementation.ai_action_interface import *
from erkenntnis.world_actions import *
from erkenntnis.utils import random_position


def test_action_encoding_action_conversions():
    action = action_accelerate(direction=random_position(), strength=0.6)
    encoded = action_to_numeric_encoding(action=action)
    action2 = numeric_encoding_to_action(encoding=encoded)
    assert(action == action2)

    # action = action_point_out(agent_direction=random_position(), pointing_direction=random_position(), reason=0.88)
    # encoded = action_to_numeric_encoding(action=action)
    # action2 = numeric_encoding_to_action(encoding=encoded)
    # assert(action == action2)

    action = action_point_out(agent_direction=random_position(), pointing_direction=random_position(), reason=0.88)
    encoded = action_to_numeric_encoding(action=action)
    action2 = numeric_encoding_to_action(encoding=encoded)
    assert(action == action2)


def test_encoding_action_encoding_conversions():
    encoded, _ = get_numeric_encoding_and_action_indices(available_actions=available_actions)
    encoded[4] = 1.0    # focus
    action = numeric_encoding_to_action(encoding=encoded)
    encoded2 = action_to_numeric_encoding(action=action)
    assert(encoded == encoded2)

    encoded, _ = get_numeric_encoding_and_action_indices(available_actions=available_actions)
    encoded[5] = 1.0    # remove malus
    action = numeric_encoding_to_action(encoding=encoded)
    encoded2 = action_to_numeric_encoding(action=action)
    assert(encoded == encoded2)

    encoded, _ = get_numeric_encoding_and_action_indices(available_actions=available_actions)
    encoded[16] = 1.0   # push
    encoded[17] = 0.7
    encoded[18] = 0.57
    encoded[19] = 0.1
    action = numeric_encoding_to_action(encoding=encoded)
    encoded2 = action_to_numeric_encoding(action=action)
    assert(encoded == encoded2)



def test_action_encoding_conversions():
    action = action_accelerate(direction=random_position(), strength=0.6)
    print(action)
    offset = 0
    encoded = action_to_numeric_encoding(action)
    assert(encoded[offset + 0] == 1.0)
    assert(encoded[offset + 1] == action["direction"][0])
    assert(encoded[offset + 2] == action["direction"][1])
    assert(encoded[offset + 3] == action["strength"])

    action = action_attack(direction=random_position(), strength=0.4)
    offset = 24
    encoded = action_to_numeric_encoding(action)
    assert(encoded[offset + 0] == 1.0)
    assert(encoded[offset + 1] == action["direction"][0])
    assert(encoded[offset + 2] == action["direction"][1])
    assert(encoded[offset + 3] == action["strength"])
    
    action = action_eat(direction=random_position(), strength=0.2)
    offset = 28
    encoded = action_to_numeric_encoding(action)
    assert(encoded[offset + 0] == 1.0)
    assert(encoded[offset + 1] == action["direction"][0])
    assert(encoded[offset + 2] == action["direction"][1])
    assert(encoded[offset + 3] == action["strength"])

    action = action_inform_malus(direction=random_position())
    offset = 6  # inform malus = communicate, --> 7 - 1
    assert(encoded[offset + 0] == 1.0)
    assert(encoded[offset + 1] == action["direction"][0])
    assert(encoded[offset + 2] == action["direction"][1])
    # assert(encoded[offset + 3] == action["message"])
    assert(encoded[offset + 3] == 1.0)

    action = action_communicate(direction=random_position(), message="lol_test")
    offset = 6  # communicate, --> 7 - 1
    assert(encoded[offset + 0] == 1.0)
    assert(encoded[offset + 1] == action["direction"][0])
    assert(encoded[offset + 2] == action["direction"][1])
    # assert(encoded[offset + 3] == action["message"])
    assert(encoded[offset + 3] == 0.2)

    action = action_communicate(direction=random_position(), message=0.57)
    offset = 6  # communicate, --> 7 - 1
    assert(encoded[offset + 0] == 1.0)
    assert(encoded[offset + 1] == action["direction"][0])
    assert(encoded[offset + 2] == action["direction"][1])
    assert(encoded[offset + 3] == action["message"])
