import numpy as np
import copy


def obstruct_perception(position, raw_perception):
    perception = list()
    for thing in raw_perception:
        perceived_thing = _copy_and_clean_percieved_thing(thing=thing)
        perceived_thing.position = perceived_thing.position - position
        perception.append(perceived_thing)
    # print("TODO: the perception of objects needs to change if obstruction/mirroring happens")
    return perception


def _copy_and_clean_percieved_thing(thing):
    perceived_thing = copy.deepcopy(thing)
    try:
        perceived_thing.behavior = None
    except Exception:
        pass
    try:
        perceived_thing.messages = None
    except Exception:
        pass
    return perceived_thing


# TODO: remove perceiving agent (otherwise agents could see the malus on them)
def perception_at_position(all_things, position, radius):
    _minimal_perception_range = 0.000001    # used to exclude agents from their perception, but could be used to hide?
    raw_perception = []
    for this_thing in all_things:
        dist = np.linalg.norm(position - this_thing.position)
        if dist < radius and dist > _minimal_perception_range:
            raw_perception.append(this_thing)
    perception = obstruct_perception(position=position, raw_perception=raw_perception)
    return perception, raw_perception
