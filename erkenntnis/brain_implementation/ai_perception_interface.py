import numpy as np
from ..thing import Thing
from .ai_action_interface import action_to_numeric_encoding, numeric_encoding_to_action
from ..world_map import _type_encoding
from ..utils import random_position
import uuid

# list of messages

properties_to_encode = {"health": 1,
                        "malus": 1,
                        "max_speed": 1,
                        "position": 2,
                        "strength": 1,
                        "type_properties": 1,
                        "unique_properties": 1,
                        "velocity": 2,
                        "action_cooldown": 1,   # agent specifics
                        # "last_action": 35,       # depends on the number of actions, currently 35
                        "last_action": 17,       # depends on the number of actions, 17 for limited action set
                        "last_cause": 1
                        # "up to 3 messages": 3*2,
                        }


def _encoding_length(properties_to_encode: dict):
    encoding_length = 0
    for property in properties_to_encode:
        encoding_length += properties_to_encode[property]
    return encoding_length


def _encode_type_properties(type):
    try:
        type_encoding = _type_encoding[type]
    except KeyError:
        type_encoding = _type_encoding["unknown"]
    return type_encoding


def _decode_type_properties(encoded_type):
    type_decoding = {value: key for key, value in _type_encoding.items()}
    original_type = type_decoding[encoded_type]
    return original_type


def _encode_unique_name(unique_properties):
    if unique_properties is None:
        return 0
    return unique_properties

    # print(unique_properties)
    # number = int(unique_properties)
    # print(number)
    # # TODO we could just enum the things in a world?
    # return number

def _decode_unique_name(encoded_unique):
    if encoded_unique == 0:
        return None
    return encoded_unique


def _perceived_thing_to_encoding(thing: Thing):
    encoding_length = _encoding_length(properties_to_encode=properties_to_encode)
    encoding = np.zeros(encoding_length)

    encoding[0] = thing.health
    encoding[1] = thing.malus
    encoding[2] = thing.max_speed
    encoding[3] = thing.position[0]
    encoding[4] = thing.position[1]
    encoding[5] = thing.strength
    encoding[6] = _encode_type_properties(thing.type_properties)
    encoding[7] = _encode_unique_name(thing.unique_properties)
    encoding[8] = thing.velocity[0]
    encoding[9] = thing.velocity[1]

    # due to circular import, we need to check if the thing is an agent without explicitly using the Agent definition
    # if isinstance(thing, Agent):
    is_agent = False
    try:
        temp = thing.last_action
        is_agent = True
    except Exception:
        pass
    if is_agent:
        encoding[10] = thing.action_cooldown
        encoding[11] = _encode_unique_name(thing.last_cause)
        last_encoded_action = action_to_numeric_encoding(thing.last_action)
        encoding[12:12 + 17] = last_encoded_action[:]
    return encoding


def encode_perception(perception, expected_number_perceptions: int = 0):
    encoding_length = _encoding_length(properties_to_encode=properties_to_encode)
    if len(perception) == 0:
        if expected_number_perceptions == 0:
            return None
        else:
            return np.zeros(expected_number_perceptions * encoding_length)

    encodings = list()
    for thing in perception:
        encodings.append(_perceived_thing_to_encoding(thing))
    # TODO: maybe encode every perception as channel, because the interpretation of each channel would be the same
    encoded_perception = np.concatenate(encodings, axis=0)

    # pad the perception if the interface requires more
    if expected_number_perceptions > 0:    
        total_length = expected_number_perceptions * encoding_length
        missing_padding = total_length - encoded_perception.shape[0]
        encoded_perception = np.pad(encoded_perception, (0, missing_padding), 'constant', constant_values=0.0)

    return encoded_perception


def decode_perceived_thing(encoding: np.ndarray):
    encoding_length = _encoding_length(properties_to_encode=properties_to_encode)
    assert(encoding.shape[0] == encoding_length)

    if (np.sum(encoding) == 0.0):
        return None

    type_properties = _decode_type_properties(encoding[6])

    thing = Thing(position=random_position())
    thing.health = encoding[0]
    thing.malus = encoding[1]
    thing.max_speed = encoding[2]
    thing.position = np.array([encoding[3], encoding[4], 0.0])
    thing.strength = encoding[5]
    thing.type_properties = type_properties
    thing.unique_properties = _decode_unique_name(encoding[7])
    thing.velocity = np.array([encoding[8], encoding[9], 0.0])

    if type_properties in ["dummy", "sheep", "wolf", "monkey", "ape"]:
        thing.action_cooldown = encoding[10]
        thing.last_cause = _decode_unique_name(encoding[11])
        thing.last_action = numeric_encoding_to_action(encoding[12:12 + 17])

    return thing


def decode_perception(encoded_perception: np.ndarray):
    encoding_length = _encoding_length(properties_to_encode=properties_to_encode)
    assert(encoded_perception.shape[0] % encoding_length == 0)
    number_encoded_things = int(encoded_perception.shape[0] / encoding_length)
    assert(encoding_length * number_encoded_things == encoded_perception.shape[0])

    perception = []
    for i in range(number_encoded_things):
        encoded_thing = encoded_perception[i * encoding_length: (i + 1) * encoding_length]
        perceived_thing = decode_perceived_thing(encoding=encoded_thing)
        if perceived_thing is not None:
            perception.append(perceived_thing)

    return perception


    









