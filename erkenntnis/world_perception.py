import numpy as np
import copy


def obstruct_perception(position, perception):
    # print("TODO: the perception of objects needs to change if obstruction/mirroring happens")
    return perception


def perception_at_position(all_things, position, radius):
    raw_perception = []
    for this_thing in all_things:
        dist = np.linalg.norm(position - this_thing.position)
        if dist < radius:
            raw_perception.append(this_thing)
    perception = obstruct_perception(position=position, perception=raw_perception)
    return perception, raw_perception
