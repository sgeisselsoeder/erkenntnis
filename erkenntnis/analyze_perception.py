import numpy as np
from .thing import Thing
from .utils import vector_length


def split_perception_by_type(perception):
    split_perception = {}
    # split by type
    for thing in perception:
        thing_type = thing.type_properties
        if thing_type not in split_perception:
            split_perception[thing_type] = list()

        split_perception[thing_type].append(thing)

    # sort by distance
    for thing_type in split_perception:
        split_perception[thing_type].sort(key=lambda x: vector_length(x.position))

    return split_perception
