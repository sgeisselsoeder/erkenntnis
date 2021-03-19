import numpy as np
from ..available_actions import _available_actions

_message_encoding_default = 0.5


def get_numeric_encoding_and_action_indices(available_actions: dict):
    action_indices = {}
    parameter_count = 0
    for action_name in available_actions:
        action_indices[action_name] = parameter_count
        parameter_count += 1    # the action itself
        if available_actions[action_name] is not None:
            parameter_count += len(available_actions[action_name])    # the parameters of this action
    numeric_action_encoding = np.zeros(parameter_count, dtype=np.float32)
    return numeric_action_encoding, action_indices


def action_to_numeric_encoding(action, available_actions=_available_actions):
    encoding, action_indices = get_numeric_encoding_and_action_indices(available_actions=available_actions)
    if action is None:
        return encoding

    action_index = action_indices[action["type"]]
    encoding[action_index] = 1.0    # mark the action to use

    if action["type"] == "accelerate":
        encoding[action_index + 1] = action["direction"][0]
        encoding[action_index + 2] = action["direction"][1]
        encoding[action_index + 3] = action["strength"]

    elif action["type"] == "focus":
        pass

    elif action["type"] == "remove_malus":
        pass

    elif action["type"] == "communicate":
        encoding[action_index + 1] = action["direction"][0]
        encoding[action_index + 2] = action["direction"][1]
        try:
            encoding[action_index + 3] = float(action["message"])
        except Exception:
            encoding[action_index + 3] = _message_encoding_default

    elif action["type"] == "inform_malus":
        encoding[action_index + 1] = action["direction"][0]
        encoding[action_index + 2] = action["direction"][1]

    elif action["type"] == "point":
        encoding[action_index + 1] = action["agent_direction"][0]
        encoding[action_index + 2] = action["agent_direction"][1]
        encoding[action_index + 3] = action["pointing_direction"][0]
        encoding[action_index + 4] = action["pointing_direction"][1]
        try:
            encoding[action_index + 5] = float(action["reason"])
        except Exception:
            encoding[action_index + 5] = _message_encoding_default

    elif action["type"] == "push":
        encoding[action_index + 1] = action["direction"][0]
        encoding[action_index + 2] = action["direction"][1]
        encoding[action_index + 3] = action["strength"]

    elif action["type"] == "pull":
        encoding[action_index + 1] = action["direction"][0]
        encoding[action_index + 2] = action["direction"][1]
        encoding[action_index + 3] = action["strength"]

    elif action["type"] == "attack":
        encoding[action_index + 1] = action["direction"][0]
        encoding[action_index + 2] = action["direction"][1]
        encoding[action_index + 3] = action["strength"]

    elif action["type"] == "eat":
        encoding[action_index + 1] = action["direction"][0]
        encoding[action_index + 2] = action["direction"][1]
        encoding[action_index + 3] = action["strength"]

    else:
        raise("Unrecognized action " + str(action["type"]))

    return encoding


def numeric_encoding_to_action(encoding, available_actions=_available_actions):
    _, action_indices = get_numeric_encoding_and_action_indices(available_actions=available_actions)

    max_action_value = 0.0
    for action_name in action_indices:
        current_action_index = action_indices[action_name]
        activation_strength = encoding[current_action_index]
        if activation_strength > max_action_value:
            max_action_value = activation_strength
            selected_action = action_name
            action_index = current_action_index

    # None action should be encoded as entirely zeros
    if max_action_value == 0.0:
        action = None
        return action

    action = {"type": selected_action}

    if selected_action == "accelerate":
        action["direction"] = np.array([encoding[action_index + 1], encoding[action_index + 2], 0.0], dtype=np.float32)
        action["strength"] = encoding[action_index + 3]

    elif selected_action == "focus":
        pass

    elif selected_action == "remove_malus":
        pass

    elif selected_action == "communicate":
        action["direction"] = np.array([encoding[action_index + 1], encoding[action_index + 2], 0.0])
        action["message"] = encoding[action_index + 3]

    elif selected_action == "inform_malus":
        action["direction"] = np.array([encoding[action_index + 1], encoding[action_index + 2], 0.0])
        action["message"] = "malus"

    elif selected_action == "point":
        action["agent_direction"] = np.array([encoding[action_index + 1], encoding[action_index + 2], 0.0])
        action["pointing_direction"] = np.array([encoding[action_index + 3], encoding[action_index + 4], 0.0])
        action["reason"] = encoding[action_index + 5]

    elif selected_action == "push":
        action["direction"] = np.array([encoding[action_index + 1], encoding[action_index + 2], 0.0])
        action["strength"] = encoding[action_index + 3]

    elif selected_action == "pull":
        action["direction"] = np.array([encoding[action_index + 1], encoding[action_index + 2], 0.0])
        action["strength"] = encoding[action_index + 3]

    elif selected_action == "attack":
        action["direction"] = np.array([encoding[action_index + 1], encoding[action_index + 2], 0.0])
        action["strength"] = encoding[action_index + 3]

    elif selected_action == "eat":
        action["direction"] = np.array([encoding[action_index + 1], encoding[action_index + 2], 0.0])
        action["strength"] = encoding[action_index + 3]

    else:
        raise("Unrecognized action " + str(selected_action))

    return action
