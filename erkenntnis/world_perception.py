import numpy as np
import copy


def obstruct_perception(position, perception):
    # print("TODO: the perception of objects needs to change if obstruction/mirroring happens")
    return perception


# TODO: remove perceiving agent (otherwise agents could see the malus on them)
def perception_at_position(all_things, position, radius):
    raw_perception = []
    for this_thing in all_things:
        dist = np.linalg.norm(position - this_thing.position)
        if dist < radius:
            perceived_thing = copy.deepcopy(this_thing)
            perceived_thing["position"] = position - perceived_thing["position"]
            raw_perception.append(perceived_thing)
    perception = obstruct_perception(position=position, perception=raw_perception)
    return perception, raw_perception
