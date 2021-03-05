from erkenntnis.brain_implementation.ai_perception_interface import *
from erkenntnis.brain_implementation.ai_perception_interface import _encoding_length
from erkenntnis.world import World
from erkenntnis.agents_available import *
from erkenntnis.things_available import new_grass
from erkenntnis.world_actions import action_accelerate, action_remove_malus
from erkenntnis.utils import random_position

    
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
    assert(encoded_perception[0] == agent.health)
    assert(encoded_perception[1] == agent.malus)
    assert(encoded_perception[2] == agent.max_speed)
    assert(encoded_perception[3] == agent.position[0])
    assert(encoded_perception[4] == agent.position[1])
    assert(encoded_perception[5] == agent.strength)
    # assert(encoded_perception[6] == agent.health)
    # assert(encoded_perception[7] == agent.health)
    assert(encoded_perception[8] == agent.velocity[0])
    assert(encoded_perception[9] == agent.velocity[1])
    assert(encoded_perception[10] == agent.action_cooldown)
    # assert(encoded_perception[11] == agent.health)
    assert(np.sum(encoded_perception[12:]) == 0.0)


def test_grass_encoding():
    thing = new_grass()
    perception = [thing]
    encoded_perception = encode_perception(perception=perception)
    expected_length = _encoding_length(properties_to_encode=properties_to_encode)
    assert(encoded_perception.shape[0] == expected_length)
    assert(encoded_perception[0] == thing.health)
    assert(encoded_perception[1] == thing.malus)
    assert(encoded_perception[2] == thing.max_speed)
    assert(encoded_perception[3] == thing.position[0])
    assert(encoded_perception[4] == thing.position[1])
    assert(encoded_perception[5] == thing.strength)
    assert(encoded_perception[8] == thing.velocity[0])
    assert(encoded_perception[9] == thing.velocity[1])
    assert(np.sum(encoded_perception[10:]) == 0.0)


def test_wolf_encoding_with_accel_action():
    agent = new_wolf()
    agent.last_action = action_accelerate(direction=random_position())
    perception = [agent]
    encoded_perception = encode_perception(perception=perception)
    expected_length = _encoding_length(properties_to_encode=properties_to_encode)
    assert(encoded_perception.shape[0] == expected_length)
    assert(encoded_perception[0] == agent.health)
    assert(encoded_perception[1] == agent.malus)
    assert(encoded_perception[2] == agent.max_speed)
    assert(encoded_perception[3] == agent.position[0])
    assert(encoded_perception[4] == agent.position[1])
    assert(encoded_perception[5] == agent.strength)
    assert(encoded_perception[8] == agent.velocity[0])
    assert(encoded_perception[9] == agent.velocity[1])
    assert(encoded_perception[10] == agent.action_cooldown)
    assert(encoded_perception[12] == 1.0)
    assert(encoded_perception[15] == 1.0)


def test_monkey_encoding_with_malus_action():
    agent = new_monkey()
    agent.last_action = action_remove_malus()
    perception = [agent]
    encoded_perception = encode_perception(perception=perception)
    expected_length = _encoding_length(properties_to_encode=properties_to_encode)
    assert(encoded_perception.shape[0] == expected_length)
    assert(encoded_perception[0] == agent.health)
    assert(encoded_perception[1] == agent.malus)
    assert(encoded_perception[2] == agent.max_speed)
    assert(encoded_perception[3] == agent.position[0])
    assert(encoded_perception[4] == agent.position[1])
    assert(encoded_perception[5] == agent.strength)
    assert(encoded_perception[8] == agent.velocity[0])
    assert(encoded_perception[9] == agent.velocity[1])
    assert(encoded_perception[10] == agent.action_cooldown)
    assert(np.sum(encoded_perception[12:]) > 0.0)


def test_monkey_encoding_padding():
    agent = new_monkey()
    perception = [agent]
    encoded_perception = encode_perception(perception=perception, expected_number_perceptions=5)
    expected_length = _encoding_length(properties_to_encode=properties_to_encode)
    assert(encoded_perception.shape[0] == 5 * expected_length)
    assert(encoded_perception[0] == agent.health)
    assert(encoded_perception[1] == agent.malus)
    assert(encoded_perception[2] == agent.max_speed)
    assert(encoded_perception[3] == agent.position[0])
    assert(encoded_perception[4] == agent.position[1])
    assert(encoded_perception[5] == agent.strength)
    assert(encoded_perception[8] == agent.velocity[0])
    assert(encoded_perception[9] == agent.velocity[1])
    assert(encoded_perception[10] == agent.action_cooldown)
    assert(np.sum(encoded_perception[12:]) == 0.0)


def test_encoding_in_scenario():
    pass
    # my_world = World(malus_propability=0.0)

    # my_world.add(new_sheep(), position=np.array([1.0, 0.0, 0.0]))
    # my_world.add(new_wolf(), position=np.array([2.0, 2.0, 0.0]))
    # for i in range(100):
    #     my_world.run(time_delta=0.1)

    # assert(len(my_world.things) == 0)
    # assert(len(my_world.agents) == 1)
    # assert(my_world.agents[0].type_properties == "wolf")
    # assert(my_world.agents[0].health >= 140.0)
