# TODO: generate a world model to "understand" its state.
# possibly by autoencoder?

class Worldmodel():
    def __init__(self):
        self.model = None

    def retrain_model(self, perceptions):
        self.model.train(perceptions)

    def comprehend_state(self, encoded_perception, encoded_messages, last_states, last_actions):
        total_perception = encoded_perception + encoded_messages + last_states + last_actions
        # TODO: split perceptions into things again and feed as channels?
        latent_space_result = self.model.apply(total_perception)
        return latent_space_result

    def estimate_future_state(self, encoded_perception, encoded_messages, last_states, last_actions, next_action):
        future_state = None
        return future_state
