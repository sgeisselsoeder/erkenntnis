from erkenntnis.brain_implementation.ai_perception_interface import *
from erkenntnis.brain_implementation.ai_perception_interface import _encoding_length, _encode_type_properties
from erkenntnis.agents_available import new_ape, new_monkey, new_sheep, new_wolf
from erkenntnis.things_available import new_grass, new_stone
from erkenntnis.world_actions import action_accelerate, action_remove_malus
from erkenntnis.utils import random_position, assert_approx_equal


def test_encoding_length():
    # this test is required, as the format is hardcoded
    expected_length = _encoding_length(properties_to_encode=properties_to_encode)
    assert(expected_length == 29)


def test_sheep_encoding_no_action():
    agent = new_sheep()
    perception = [agent]
    encoded_perception = encode_perception(perception=perception)
    expected_length = _encoding_length(properties_to_encode=properties_to_encode)
    assert(encoded_perception.shape[0] == expected_length)
    assert_approx_equal(encoded_perception[0], agent.health)
    assert_approx_equal(encoded_perception[1], agent.malus)
    assert_approx_equal(encoded_perception[2], agent.max_speed)
    assert_approx_equal(encoded_perception[3], agent.position[0])
    assert_approx_equal(encoded_perception[4], agent.position[1])
    assert_approx_equal(encoded_perception[5], agent.strength)
    assert_approx_equal(encoded_perception[6], _encode_type_properties(agent.type_properties))

    assert_approx_equal(encoded_perception[8], agent.velocity[0])
    assert_approx_equal(encoded_perception[9], agent.velocity[1])
    assert_approx_equal(encoded_perception[10], agent.action_cooldown)

    assert_approx_equal(np.sum(encoded_perception[12:]), 0.0)
    # assert(encoded_perception[0] == agent.health)
    # assert(encoded_perception[1] == agent.malus)
    # assert(encoded_perception[2] == agent.max_speed)
    # assert(encoded_perception[3] == agent.position[0])
    # assert(encoded_perception[4] == agent.position[1])
    # assert(encoded_perception[5] == agent.strength)
    # assert(encoded_perception[6] == _encode_type_properties(agent.type_properties))
    # # assert(encoded_perception[7] == agent.health)
    # assert(encoded_perception[8] == agent.velocity[0])
    # assert(encoded_perception[9] == agent.velocity[1])
    # assert(encoded_perception[10] == agent.action_cooldown)
    # # assert(encoded_perception[11] == agent.health)
    # assert(np.sum(encoded_perception[12:]) == 0.0)


def test_grass_encoding():
    thing = new_grass()
    perception = [thing]
    encoded_perception = encode_perception(perception=perception)
    expected_length = _encoding_length(properties_to_encode=properties_to_encode)
    assert(encoded_perception.shape[0] == expected_length)
    assert_approx_equal(encoded_perception[0], thing.health)
    assert_approx_equal(encoded_perception[1], thing.malus)
    assert_approx_equal(encoded_perception[2], thing.max_speed)
    assert_approx_equal(encoded_perception[3], thing.position[0])
    assert_approx_equal(encoded_perception[4], thing.position[1])
    assert_approx_equal(encoded_perception[5], thing.strength)
    assert_approx_equal(encoded_perception[6], _encode_type_properties(thing.type_properties))

    assert_approx_equal(encoded_perception[8], thing.velocity[0])
    assert_approx_equal(encoded_perception[9], thing.velocity[1])

    assert_approx_equal(np.sum(encoded_perception[10:]), 0.0)
    # assert(encoded_perception[0] == thing.health)
    # assert(encoded_perception[1] == thing.malus)
    # assert(encoded_perception[2] == thing.max_speed)
    # assert(encoded_perception[3] == thing.position[0])
    # assert(encoded_perception[4] == thing.position[1])
    # assert(encoded_perception[5] == thing.strength)
    # assert(encoded_perception[6] == _encode_type_properties(thing.type_properties))
    # assert(encoded_perception[8] == thing.velocity[0])
    # assert(encoded_perception[9] == thing.velocity[1])
    # assert(np.sum(encoded_perception[10:]) == 0.0)


def test_wolf_encoding_with_accel_action():
    agent = new_wolf()
    agent.last_action = action_accelerate(direction=random_position())
    perception = [agent]
    encoded_perception = encode_perception(perception=perception)
    expected_length = _encoding_length(properties_to_encode=properties_to_encode)
    assert(encoded_perception.shape[0] == expected_length)
    assert_approx_equal(encoded_perception[0], agent.health)
    assert_approx_equal(encoded_perception[1], agent.malus)
    assert_approx_equal(encoded_perception[2], agent.max_speed)
    assert_approx_equal(encoded_perception[3], agent.position[0])
    assert_approx_equal(encoded_perception[4], agent.position[1])
    assert_approx_equal(encoded_perception[5], agent.strength)
    assert_approx_equal(encoded_perception[6], _encode_type_properties(agent.type_properties))

    assert_approx_equal(encoded_perception[8], agent.velocity[0])
    assert_approx_equal(encoded_perception[9], agent.velocity[1])
    assert_approx_equal(encoded_perception[10], agent.action_cooldown)

    assert_approx_equal(encoded_perception[12], 1.0)
    assert_approx_equal(encoded_perception[15], 1.0)

    # assert(encoded_perception[0] == agent.health)
    # assert(encoded_perception[1] == agent.malus)
    # assert(encoded_perception[2] == agent.max_speed)
    # assert(encoded_perception[3] == agent.position[0])
    # assert(encoded_perception[4] == agent.position[1])
    # assert(encoded_perception[5] == agent.strength)
    # assert(encoded_perception[6] == _encode_type_properties(agent.type_properties))
    # assert(encoded_perception[8] == agent.velocity[0])
    # assert(encoded_perception[9] == agent.velocity[1])
    # assert(encoded_perception[10] == agent.action_cooldown)
    # assert(encoded_perception[12] == 1.0)
    # assert(encoded_perception[15] == 1.0)


def test_monkey_encoding_with_malus_action():
    agent = new_ape()
    agent.last_action = action_remove_malus()
    perception = [agent]
    encoded_perception = encode_perception(perception=perception)
    expected_length = _encoding_length(properties_to_encode=properties_to_encode)
    assert(encoded_perception.shape[0] == expected_length)
    assert_approx_equal(encoded_perception[0], agent.health)
    assert_approx_equal(encoded_perception[1], agent.malus)
    assert_approx_equal(encoded_perception[2], agent.max_speed)
    assert_approx_equal(encoded_perception[3], agent.position[0])
    assert_approx_equal(encoded_perception[4], agent.position[1])
    assert_approx_equal(encoded_perception[5], agent.strength)
    assert_approx_equal(encoded_perception[6], _encode_type_properties(agent.type_properties))

    assert_approx_equal(encoded_perception[8], agent.velocity[0])
    assert_approx_equal(encoded_perception[9], agent.velocity[1])
    assert_approx_equal(encoded_perception[10], agent.action_cooldown)

    # assert(encoded_perception[0] == agent.health)
    # assert(encoded_perception[1] == agent.malus)
    # assert(encoded_perception[2] == agent.max_speed)
    # assert(encoded_perception[3] == agent.position[0])
    # assert(encoded_perception[4] == agent.position[1])
    # assert(encoded_perception[5] == agent.strength)
    # assert(encoded_perception[6] == _encode_type_properties(agent.type_properties))
    # assert(encoded_perception[8] == agent.velocity[0])
    # assert(encoded_perception[9] == agent.velocity[1])
    # assert(encoded_perception[10] == agent.action_cooldown)
    assert(np.sum(encoded_perception[12:]) > 0.0)


def test_monkey_encoding_padding():
    agent = new_monkey()
    perception = [agent]
    encoded_perception = encode_perception(perception=perception, expected_number_perceptions=5)
    expected_length = _encoding_length(properties_to_encode=properties_to_encode)
    assert(encoded_perception.shape[0] == 5 * expected_length)
    assert_approx_equal(encoded_perception[0], agent.health)
    assert_approx_equal(encoded_perception[1], agent.malus)
    assert_approx_equal(encoded_perception[2], agent.max_speed)
    assert_approx_equal(encoded_perception[3], agent.position[0])
    assert_approx_equal(encoded_perception[4], agent.position[1])
    assert_approx_equal(encoded_perception[5], agent.strength)
    assert_approx_equal(encoded_perception[6], _encode_type_properties(agent.type_properties))

    assert_approx_equal(encoded_perception[8], agent.velocity[0])
    assert_approx_equal(encoded_perception[9], agent.velocity[1])
    assert_approx_equal(encoded_perception[10], agent.action_cooldown)
    assert_approx_equal(np.sum(encoded_perception[12:]), 0.0)
    # assert(encoded_perception[0] == agent.health)
    # assert(encoded_perception[1] == agent.malus)
    # assert(encoded_perception[2] == agent.max_speed)
    # assert(encoded_perception[3] == agent.position[0])
    # assert(encoded_perception[4] == agent.position[1])
    # assert(encoded_perception[5] == agent.strength)
    # assert(encoded_perception[6] == _encode_type_properties(agent.type_properties))
    # assert(encoded_perception[8] == agent.velocity[0])
    # assert(encoded_perception[9] == agent.velocity[1])
    # assert(encoded_perception[10] == agent.action_cooldown)
    # assert(np.sum(encoded_perception[12:]) == 0.0)


def test_empty_encoding():
    perception = []
    encoded_perception = encode_perception(perception=perception, expected_number_perceptions=2)
    expected_length = _encoding_length(properties_to_encode=properties_to_encode)
    assert(encoded_perception.shape[0] == 2 * expected_length)
    assert(np.sum(encoded_perception) == 0.0)


def test_thing_perception_encode_decode():
    thing = new_stone()
    perception = [thing]
    encoded_perception = encode_perception(perception=perception, expected_number_perceptions=5)
    decoded_perception = decode_perception(encoded_perception=encoded_perception)
    assert(len(decoded_perception) == len(perception))
    assert(len(decoded_perception) == 1)

    decoded_thing = decoded_perception[0]
    assert_approx_equal(thing.health, decoded_thing.health)
    assert_approx_equal(thing.malus, decoded_thing.malus)
    assert_approx_equal(thing.max_speed, decoded_thing.max_speed)
    assert_approx_equal(thing.position, decoded_thing.position)
    assert_approx_equal(thing.strength, decoded_thing.strength)
    assert_approx_equal(thing.type_properties, decoded_thing.type_properties)
    assert_approx_equal(thing.velocity, decoded_thing.velocity)

    # assert(thing.health == decoded_thing.health)
    # assert(thing.malus == decoded_thing.malus)
    # assert(thing.max_speed == decoded_thing.max_speed)
    # assert(np.all(thing.position == decoded_thing.position))
    # assert(thing.strength == decoded_thing.strength)
    # assert(thing.type_properties == decoded_thing.type_properties)
    # assert(np.all(thing.velocity == decoded_thing.velocity))


def test_agent_perception_encode_decode():
    agent = new_sheep()
    perception = [agent]
    encoded_perception = encode_perception(perception=perception, expected_number_perceptions=5)
    decoded_perception = decode_perception(encoded_perception=encoded_perception)
    assert(len(decoded_perception) == len(perception))
    assert(len(decoded_perception) == 1)

    decoded_agent = decoded_perception[0]
    assert_approx_equal(agent.health, decoded_agent.health)
    assert_approx_equal(agent.malus, decoded_agent.malus)
    assert_approx_equal(agent.max_speed, decoded_agent.max_speed)
    assert_approx_equal(agent.position, decoded_agent.position)
    assert_approx_equal(agent.strength, decoded_agent.strength)
    assert_approx_equal(agent.type_properties, decoded_agent.type_properties)
    assert_approx_equal(agent.velocity, decoded_agent.velocity)
    assert_approx_equal(agent.action_cooldown, decoded_agent.action_cooldown)
    assert_approx_equal(agent.last_action, decoded_agent.last_action)
    assert_approx_equal(agent.last_cause, decoded_agent.last_cause)

    # assert(agent.health == decoded_agent.health)
    # assert(agent.malus == decoded_agent.malus)
    # assert(agent.max_speed == decoded_agent.max_speed)
    # assert(np.all(agent.position == decoded_agent.position))
    # assert(agent.strength == decoded_agent.strength)
    # assert(agent.type_properties == decoded_agent.type_properties)
    # assert(np.all(agent.velocity == decoded_agent.velocity))
    # assert(agent.action_cooldown == decoded_agent.action_cooldown)
    # assert(agent.last_action == decoded_agent.last_action)
    # assert(agent.last_cause == decoded_agent.last_cause)
