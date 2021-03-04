import numpy as np


def _find_used_dimensions(all_things):
    # initialize with reasonable? default size
    maxpos = np.array([1.0, 1.0, 1.0])
    minpos = np.array([-1.0, -1.0, 0.0])

    for thing in all_things:
        minpos = np.minimum(minpos, thing.position)
        maxpos = np.maximum(maxpos, thing.position)
    return minpos, maxpos


def get_index(position, minpos, maxpos, size):
    dimensions = maxpos - minpos
    spacing = dimensions / np.float(size - 1)
    index = (position - minpos) / spacing
    index = index.astype(int)

    for value in index[:2]:
        assert value < size
        try:
            assert value >= 0
        except Exception:
            print("DEBUG world map")
            print(position)
            print(minpos)
            print(maxpos)
            print(size)
            print(value)
            assert value >= 0
    return index


_type_encoding = {"nothing": 0,
                  "unknown": -99,
                  "thing": -1,
                  "agent": -2,
                  "stone": 1,
                  "grass": 2,
                  "mirror": 3,
                  "dummy": 4,
                  "sheep": 5,
                  "wolf": 6,
                  "ape": 7,
                  "monkey": 8
                  }

_type_encoding_print = {"nothing": ".",
                        "unknown": "-",
                        "thing": "*",
                        "agent": "+",
                        "stone": "O",
                        "grass": "G",
                        "mirror": "~",
                        "dummy": "D",
                        "sheep": "S",
                        "wolf": "W",
                        "ape": "A",
                        "monkey": "M"
                        }

_type_encoding_print_agents = {"nothing": " ",
                               "unknown": "-",
                               "thing": "*",
                               "agent": "+",
                               "stone": "o",
                               "grass": ".",
                               "mirror": "~",
                               "dummy": "D",
                               "sheep": "S",
                               "wolf": "W",
                               "ape": "A",
                               "monkey": "M"
                               }

# _type_encoding_print = {"nothing": " . ",
#                         "unknown": " - ",
#                         "thing": " * ",
#                         "agent": " + ",
#                         "stone": " O ",
#                         "grass": " G ",
#                         "mirror": " M ",
#                         "dummy": " D ",
#                         "sheep": " S ",
#                         "wolf": " W ",
#                         "ape": " A ",
#                         "monkey": " A2"
#                         }

# _type_encoding_print_agents = {"nothing": "   ",
#                                "unknown": " - ",
#                                "thing": " * ",
#                                "agent": " + ",
#                                "stone": " o ",
#                                "grass": " . ",
#                                "mirror": " M ",
#                                "dummy": " D ",
#                                "sheep": " S ",
#                                "wolf": " W ",
#                                "ape": " A ",
#                                "monkey": " A2"
#                                }


def encode_type(type_properties: str):
    try:
        encoding = _type_encoding[type_properties]
        return encoding
    except Exception:
        raise("Unknown thing of type" + str(type_properties))


def _thing_in_boundaries(thing, boundaries):
    temp = thing.position > boundaries
    temp2 = thing.position < -boundaries
    return not (np.any(temp) or np.any(temp2))


def get_map_fixed_boundaries(all_things, size: int = 20, fixed_boundary: float = None):
    minpos = np.array([-fixed_boundary, -fixed_boundary, -fixed_boundary])
    maxpos = np.array([fixed_boundary, fixed_boundary, fixed_boundary])

    map = np.zeros((size, size), dtype=int)
    for thing in all_things:
        if _thing_in_boundaries(thing=thing, boundaries=fixed_boundary):
            index = get_index(position=thing.position, minpos=minpos, maxpos=maxpos, size=size)
            encoding = encode_type(thing.type_properties)
            map[index[0], index[1]] = encoding
    return map


def get_map_dynamic_boundaries(all_things, size: int = 20):
    minpos, maxpos = _find_used_dimensions(all_things=all_things)

    map = np.zeros((size, size), dtype=int)
    for thing in all_things:
        index = get_index(position=thing.position, minpos=minpos, maxpos=maxpos, size=size)
        encoding = encode_type(thing.type_properties)
        map[index[0], index[1]] = encoding
    return map


def get_map(all_things, size: int = 20, fixed_boundary: float = None):
    if fixed_boundary:
        return get_map_fixed_boundaries(all_things=all_things, size=size, fixed_boundary=fixed_boundary)
    else:
        return get_map_dynamic_boundaries(all_things=all_things, size=size)


def print_map(map, plotstyle: str = "sparse"):
    type_decoding = {value: key for key, value in _type_encoding.items()}
    if plotstyle == "sparse":
        print_encoding = _type_encoding_print_agents
    elif plotstyle == "dense":
        print_encoding = _type_encoding_print
    else:
        print("Unsupported map plotstyle ", plotstyle, " . Using dense.")
        print_encoding = _type_encoding_print

    map_shape = map.shape
    for i in range(map_shape[0]):
        line = ""
        for j in range(map_shape[1]):
            encoded_type = map[i, j]
            type_name = type_decoding[encoded_type]
            print_symbol = print_encoding[type_name]
            line = line + print_symbol
            line = line + " "
        print(line)
