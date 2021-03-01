import numpy as np


def _find_used_dimensions(all_things, default_dim=1.0):
    minpos = np.array([-1.0 * default_dim, -1.0 * default_dim, -1.0 * default_dim])
    maxpos = np.array([default_dim, default_dim, default_dim])
    for thing in all_things:
        minpos = np.minimum(minpos, thing.position)
        maxpos = np.maximum(maxpos, thing.position)
    return minpos, maxpos


def get_index(position, minpos, maxpos, size):
    dimensions = maxpos - minpos
    spacing = dimensions / np.float(size - 1)
    index = (position - minpos) / spacing
    index = index.astype(int)

    for value in index:
        assert value < size
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
                  "ape": 7
                  }

_type_encoding_print = {"nothing": ".",
                        "unknown": "-",
                        "thing": "*",
                        "agent": "+",
                        "stone": "O",
                        "grass": "G",
                        "mirror": "M",
                        "dummy": "D",
                        "sheep": "S",
                        "wolf": "W",
                        "ape": "A"
                        }


def encode_type(type_properties: str):
    try:
        encoding = _type_encoding[type_properties]
        return encoding
    except Exception:
        raise("Unknown thing of type" + str(type_properties))


def get_map(all_things, size: int = 20):
    minpos, maxpos = _find_used_dimensions(all_things=all_things)

    map = np.zeros((size, size), dtype=int)
    for thing in all_things:
        index = get_index(position=thing.position, minpos=minpos, maxpos=maxpos, size=size)
        encoding = encode_type(thing.type_properties)
        map[index[0], index[1]] = encoding
    return map


def print_map(map):
    # np.set_printoptions(threshold=np.inf)
    # print(map)

    type_decoding = {value: key for key, value in _type_encoding.items()}

    map_shape = map.shape
    for i in range(map_shape[0]):
        line = ""
        for j in range(map_shape[1]):
            encoded_type = map[i, j]
            type_name = type_decoding[encoded_type]
            print_symbol = _type_encoding_print[type_name]
            line = line + print_symbol + " "
        print(line)
