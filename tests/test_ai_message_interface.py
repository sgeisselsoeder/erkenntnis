from erkenntnis.brain_implementation.ai_message_interface import *
from erkenntnis.brain_implementation.ai_message_interface import _length_of_message, _encode_message, _decode_message, _message_encoding_malus, _message_encoding_default
from erkenntnis.agents_available import new_ape, new_monkey, new_sheep, new_wolf
from erkenntnis.world_actions import action_communicate, action_inform_malus
from erkenntnis.utils import random_position
from erkenntnis.world import World


def test_encoding_length():
    # this test is required, as the format is hardcoded
    assert(_length_of_message == 4)


def test_message_encoding():
    message = {"from": 123,
               "from_location": np.array([1.0, 2.0, 0.0]),
               "message": 0.4}

    encoded = _encode_message(message=message)
    assert(encoded.shape[0] == _length_of_message)
    assert(encoded[0] == message["from"])
    assert(encoded[1] == message["from_location"][0])
    assert(encoded[2] == message["from_location"][1])
    assert(encoded[3] == message["message"])


def test_messages_encoding():
    messages = []
    messages.append({"from": 123,
                     "from_location": np.array([1.0, 2.0, 0.0]),
                     "message": 0.4})
    messages.append({"from": 125,
                     "from_location": np.array([991.0, -22.0, 0.0]),
                     "message": "malus"})
    messages.append({"from": 128,
                     "from_location": np.array([-1.0, -200000000.0, 0.0]),
                     "message": "lol"})

    encoded = encode_messages(messages=messages)

    assert(encoded.shape[0] == _length_of_message * len(messages))
    assert(encoded[0] == messages[0]["from"])
    assert(encoded[1] == messages[0]["from_location"][0])
    assert(encoded[2] == messages[0]["from_location"][1])
    assert(encoded[3] == messages[0]["message"])
    assert(encoded[4] == messages[1]["from"])
    assert(encoded[5] == messages[1]["from_location"][0])
    assert(encoded[6] == messages[1]["from_location"][1])
    assert(encoded[7] == _message_encoding_malus)
    assert(encoded[8] == messages[2]["from"])
    assert(encoded[9] == messages[2]["from_location"][0])
    assert(encoded[10] == messages[2]["from_location"][1])
    assert(encoded[11] == _message_encoding_default)


def test_messages_encoding_padding():
    messages = []
    messages.append({"from": 123,
                     "from_location": np.array([1.0, 2.0, 0.0]),
                     "message": "0.6"})
    messages.append({"from": 125,
                     "from_location": np.array([991.0, -22.0, 0.0]),
                     "message": "malus"})
    messages.append({"from": 128,
                     "from_location": np.array([-1.0, -200000000.0, 0.0]),
                     "message": "fubar"})

    required_number = 5
    encoded = encode_messages(messages=messages, required_number_of_messages=required_number)

    assert(encoded.shape[0] == _length_of_message * required_number)
    assert(encoded[0] == messages[0]["from"])
    assert(encoded[1] == messages[0]["from_location"][0])
    assert(encoded[2] == messages[0]["from_location"][1])
    assert(encoded[3] == float(messages[0]["message"]))
    assert(encoded[4] == messages[1]["from"])
    assert(encoded[5] == messages[1]["from_location"][0])
    assert(encoded[6] == messages[1]["from_location"][1])
    assert(encoded[7] == _message_encoding_malus)
    assert(encoded[8] == messages[2]["from"])
    assert(encoded[9] == messages[2]["from_location"][0])
    assert(encoded[10] == messages[2]["from_location"][1])
    assert(encoded[11] == _message_encoding_default)
    assert(np.sum(encoded[12:]) == 0.0)


def test_message_decoding():
    encoded = np.array([678, 1.0, -4.0, 0.5])
    message = _decode_message(encoded=encoded)
    assert(message["from"] == encoded[0])
    assert(message["from_location"][0] == encoded[1])
    assert(message["from_location"][1] == encoded[2])
    assert(message["message"] == encoded[3])


def test_message_encoding_decoding():
    message = {"from": 123,
               "from_location": np.array([1.0, 2.0, 0.0]),
               "message": 0.5}

    encoded = _encode_message(message=message)
    decoded_message = _decode_message(encoded=encoded)
    for key in message:
        assert(np.all(message[key] == decoded_message[key]))


def test_messages_encoding_decoding():
    messages = []
    messages.append({"from": 123,
                     "from_location": np.array([1.0, 2.0, 0.0]),
                     "message": 0.5})
    messages.append({"from": 125,
                     "from_location": np.array([991.0, -22.0, 0.0]),
                     "message": "malus"})
    messages.append({"from": 128,
                     "from_location": np.array([-1.0, -200000000.0, 0.0]),
                     "message": 0.12344})

    encoded = encode_messages(messages=messages)
    decoded = decode_messages(encoded_messages=encoded)

    assert(len(decoded) == len(messages))
    for i in range(len(messages)):
        message = messages[i]
        decoded_message = decoded[i]
        for key in message:
            try:
                assert(np.all(message[key] == decoded_message[key]))
            except Exception:
                assert(float(message[key]) == float(decoded_message[key]))


def test_messages_encoding_decoding_padding():
    messages = []
    messages.append({"from": 123,
                     "from_location": np.array([1.0, 2.0, 0.0]),
                     "message": 0.5})
    messages.append({"from": 125,
                     "from_location": np.array([991.0, -22.0, 0.0]),
                     "message": "malus"})
    messages.append({"from": 128,
                     "from_location": np.array([-1.0, -200000000.0, 0.0]),
                     "message": 0.67})

    required_number = 5
    encoded = encode_messages(messages=messages, required_number_of_messages=required_number)
    decoded = decode_messages(encoded_messages=encoded)

    assert(len(decoded) == len(messages))
    for i in range(len(messages)):
        message = messages[i]
        decoded_message = decoded[i]
        for key in message:
            assert(np.all(message[key] == decoded_message[key]))


def test_real_message_scenario():
    my_world = World(agent_health_decline=0.0, malus_propability=0.0)
    my_world.add(new_monkey(), position=np.array([1.0, 0.0, 0.0]))
    my_world.add(new_monkey(), position=np.array([2.0, 2.0, 0.0]))

    for i in range(1):
        my_world.run(time_delta=0.1)

    messages1 = my_world.agents[0].messages
    assert(len(messages1) > 0)

    required_number = 5
    encoded = encode_messages(messages=messages1, required_number_of_messages=required_number)
    decoded = decode_messages(encoded_messages=encoded)

    assert(len(decoded) == len(messages1))
    for i in range(len(messages1)):
        message = messages1[i]
        decoded_message = decoded[i]
        for key in message:
            assert(np.all(message[key] == decoded_message[key]))
