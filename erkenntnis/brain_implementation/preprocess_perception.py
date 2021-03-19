import numpy as np
from ..utils import vector_length


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


def fuse_state(encoded_perception, encoded_messages, encoded_action, encoded_cause):
    if encoded_cause is None:
        encoded_cause = np.array([0.0], dtype=np.float32)
    fused_state = np.concatenate([encoded_perception, encoded_messages, encoded_action, encoded_cause])
    # fused_state = np.reshape(fused_state, (1, fused_state.shape[0]))
    return fused_state
