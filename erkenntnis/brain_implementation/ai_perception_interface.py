import numpy as np
from ..thing import Thing
from ..agent import Agent
from .ai_action_interface import action_to_numeric_encoding
from ..world_map import _type_encoding

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
    type_encoding = _type_encoding[type]
    return type_encoding


def _encode_unique_name(unique_properties):
    # TODO we could just enum the things in a world?
    return 1


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

    if isinstance(thing, Agent):
        encoding[10] = thing.action_cooldown
        encoding[11] = _encode_unique_name(thing.last_cause)
        last_encoded_action = action_to_numeric_encoding(thing.last_action)
        encoding[12:12 + 17] = last_encoded_action[:]


def encode_perception(perception):
    encodings = list()
    for thing in perception:
        encodings.append(_perceived_thing_to_encoding(thing))

    # TODO: all in one numpy array
    encoded_perception = encodings

    return encoded_perception
