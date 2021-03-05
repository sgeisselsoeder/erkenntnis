import numpy as np
import copy

from .utils import vector_length


def _obstruct_perception(position, raw_perception):
    perception = list()
    for thing in raw_perception:
        perceived_thing = _copy_and_clean_percieved_thing(thing=thing)
        perceived_thing.position = perceived_thing.position - position
        perception.append(perceived_thing)
    # print("TODO: the perception of objects needs to change if obstruction/mirroring happens")
    return perception


def _copy_and_clean_percieved_thing(thing):
    perceived_thing = copy.deepcopy(thing)
    # the brain contains memory, which contains other agents, which contains their perceptions,
    # which contains agents, which would contain a brain, which ... creates almost exponential memory consumption
    # but we don't need to see the memory or internal state of their brains, only there presence and actions
    try:
        perceived_thing.brain = None
    except Exception:
        pass

    # maybe we should see their messages?
    try:
        perceived_thing.messages = None
    except Exception:
        pass

    return perceived_thing


def _limit_number_perceived_things(perception, max_things: int = 0):
    if max_things == 0:
        return perception

    # sort by distance
    perception.sort(key=lambda x: vector_length(x.position))

    return perception[:max_things]


# TODO: remove perceiving agent (otherwise agents could see the malus on them)
def perception_at_position(all_things, position, radius, max_things: int = 0):
    _minimal_perception_range = 0.000001    # used to exclude agents from their perception, but could be used to hide?
    raw_perception = []
    for this_thing in all_things:
        dist = np.linalg.norm(position - this_thing.position)
        if dist < radius and dist > _minimal_perception_range:
            raw_perception.append(this_thing)
    perception = _obstruct_perception(position=position, raw_perception=raw_perception)
    perception = _limit_number_perceived_things(perception=perception, max_things=max_things)
    return perception, raw_perception
