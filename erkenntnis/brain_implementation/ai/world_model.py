from .autoencoder import Autoenc
from ..preprocess_perception import fuse_state
# TODO: generate a world model to "understand" its state.


class Worldmodel():
    def __init__(self):
        self.model = Autoenc(latent_space_size=0)

    #
    def train_perceptions(self, encoded_perception, encoded_messages, encoded_action, encoded_cause, epochs: int = 0):
        current_state = fuse_state(encoded_perception=encoded_perception, encoded_messages=encoded_messages,
                                   encoded_action=encoded_action, encoded_cause=encoded_cause)
        return self.train(all_perceptions=current_state, epochs=epochs)

    def train(self, all_perceptions, epochs: int = 0, verbose_level: int = 0):
        if epochs == 0:
            epochs = all_perceptions.shape[0]
        self.model.fit(x=all_perceptions, number_epochs=epochs, verbose_level=verbose_level)

    def comprehend_state(self, encoded_perception, encoded_messages, last_states, last_actions):
        total_perception = encoded_perception + encoded_messages + last_states + last_actions
        # TODO: split perceptions into things again and feed as channels?
        latent_space_result = self.model.apply(total_perception)
        return latent_space_result

    def _guess_next_actions():
        pass

    def estimate_future_state(self, encoded_perception, encoded_messages, last_states, last_actions, next_action):
        actions = self._guess_next_actions()
        future_state = None
        return future_state
