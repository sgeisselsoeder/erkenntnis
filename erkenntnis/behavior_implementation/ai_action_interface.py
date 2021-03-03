from ..world_actions import *
from ..world_actions import available_actions

# available_actions = {"accelerate": ["direction1", "direction2", "strength"],
#                     "focus": None,
#                     "remove_malus": None,
#                     "communicate": ["direction1", "direction2", "message"],
#                     "point": ["direction1", "direction2", "point_direction1", "point_direction2", "reason"],
#                     "push": ["direction1", "direction2", "strength"],
#                     "pull": ["direction1", "direction2", "strength"],
#                     "attack": ["direction1", "direction2", "strength"],
#                     "eat": ["direction1", "direction2", "strength"]}

# 0 "accelerate": [
# 1 "direction1", 
# 2 "direction2", 
# 3 "strength"],
#                     
# 4 "focus": None,
#                     
# 5 "remove_malus": None,
#                     
# 6 "communicate": [
# 7 "direction1", 
# 8 "direction2", 
# 9 "message"],
#                     
# 10 "point": [
# 11 "direction1", 
# 12 "direction2", 
# 13 "point_direction1", 
# 14 "point_direction2", 
# 15 "reason"],
#                     
# 16 "push": [
# 17 "direction1", 
# 18 "direction2", 
# 19 "strength"],
#                     
# 20 "pull": [
# 21 "direction1", 
# 22 "direction2", 
# 23 "strength"],
#                     
# 24 "attack": [
# 25 "direction1", 
# 26 "direction2", 
# 27 "strength"],
#                     
# 28 "eat": [
# 29 "direction1", 
# 30 "direction2", 
# 31 "strength"]}


def get_numeric_encoding_and_action_indices(available_actions: dict):
    action_indices = {}
    parameter_count = 0
    for action_name in available_actions:
        action_indices[action_name] = parameter_count
        parameter_count += 1    # the action itself
        if available_actions[action_name] is not None:
            parameter_count += len(available_actions[action_name]) + 1    # the parameters of this action + the action itself
    numeric_action_encoding = np.zeros(parameter_count)
    return numeric_action_encoding, action_indices


def action_to_numeric_encoding(action):
    encoding, action_indices = get_numeric_encoding_and_action_indices(available_actions=available_actions)
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

    # elif action["type"] == "inform_malus":
    #     encoding[action_index + 1] = action["direction"][0]
    #     encoding[action_index + 2] = action["direction"][1]

    elif action["type"] == "communicate":
        encoding[action_index + 1] = action["direction"][0]
        encoding[action_index + 2] = action["direction"][1]
        if action["message"] == "malus":
            encoding[action_index + 3] = 1.0
        else:
            try:
                encoding[action_index + 3] = float(action["message"])
            except Exception:
                encoding[action_index + 3] = 0.2

    elif action["type"] == "point":
        encoding[action_index + 1] = action["agent_direction"][0]
        encoding[action_index + 2] = action["agent_direction"][1]
        encoding[action_index + 3] = action["pointing_direction"][0]
        encoding[action_index + 4] = action["pointing_direction"][1]
        # encoding[action_index + 5] = action["reason"]
        try:
            encoding[action_index + 5] = float(action["reason"])
        except Exception:
            encoding[action_index + 5] = 1.0
        

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


def numeric_encoding_to_action(encoding):
    _, action_indices = get_numeric_encoding_and_action_indices(available_actions=available_actions)

    max_action_value = 0.0
    for action_name in action_indices:
        current_action_index = action_indices[action_name]
        activation_strength = encoding[current_action_index]
        if activation_strength >= max_action_value:
            max_action_value = activation_strength
            selected_action = action_name
            action_index = current_action_index
    
    action = {"type": selected_action}

    if selected_action == "accelerate":
        action["direction"] = np.array([encoding[action_index + 1], encoding[action_index + 2]])
        action["strength"] = encoding[action_index + 3]

    elif selected_action == "focus":
        pass

    elif selected_action == "remove_malus":
        pass

    # elif selected_action == "inform_malus":
    #     encoding[action_index + 1] = action["direction"][0]
    #     encoding[action_index + 2] = action["direction"][1]

    elif selected_action == "communicate":
        action["direction"] = np.array([encoding[action_index + 1], encoding[action_index + 2]])
        if np.fabs(encoding[action_index + 3] - 1.0) < 0.01:
            action["type"] = "inform_malus"
            action["message"] = "malus"
        else:
            # action["message"] = "lol"
            action["message"] = encoding[action_index + 3]

    elif selected_action == "point":
        action["agent_direction"] = np.array([encoding[action_index + 1], encoding[action_index + 2]])
        action["pointing_direction"] = np.array([encoding[action_index + 3], encoding[action_index + 4]])
        # encoding[action_index + 5] = action["reason"]
        action["reason"] = encoding[action_index + 5]

    elif selected_action == "push":
        action["direction"] = np.array([encoding[action_index + 1], encoding[action_index + 2]])
        action["strength"] = encoding[action_index + 3]

    elif selected_action == "pull":
        action["direction"] = np.array([encoding[action_index + 1], encoding[action_index + 2]])
        action["strength"] = encoding[action_index + 3]

    elif selected_action == "attack":
        action["direction"] = np.array([encoding[action_index + 1], encoding[action_index + 2]])
        action["strength"] = encoding[action_index + 3]

    elif selected_action == "eat":
        action["direction"] = np.array([encoding[action_index + 1], encoding[action_index + 2]])
        action["strength"] = encoding[action_index + 3]

    else:
        raise("Unrecognized action " + str(selected_action))

    return action
