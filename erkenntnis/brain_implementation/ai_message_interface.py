import numpy as np

_length_of_message = 4


def _encode_message(message):
    encoded = np.zeros(_length_of_message)
    encoded[0] = message["from"]
    encoded[1] = message["from_location"][0]
    encoded[2] = message["from_location"][1]
    encoded[3] = message["message"]
    return encoded


def encode_messages(messages, required_number_of_messages: int = 0):
    if required_number_of_messages > 0:
        encoded_messages = np.zeros(required_number_of_messages * _length_of_message)
    else:
        encoded_messages = np.zeros(len(messages) * _length_of_message)

    for i in range(len(messages)):
        encoded_messages[i:i + _length_of_message] = _encode_message(message=messages[i])

    return encoded_messages


def _decode_message(encoded):
    if np.sum(encoded == 0.0):
        return None

    message = {}
    message["from"] = encoded[0]
    message["from_location"] = np.array([encoded[1], encoded[2], 0.0])
    message["message"] = encoded[3]
    return message


def decode_messages(encoded_messages):
    messages = []

    assert(encoded_messages.shape[0] % _length_of_message == 0)
    number_messages = encoded_messages.shape[0] / _length_of_message

    for i in number_messages:
        encoded_message = encoded_messages[i * _length_of_message: (i + 1) * _length_of_message]
        message = _decode_message(encoded=encoded_message)
        if message is not None:
            messages.append(message)
    
    return messages
