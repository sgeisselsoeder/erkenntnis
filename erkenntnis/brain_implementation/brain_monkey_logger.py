from .brain_monkey_hardcoded import Brain_monkey_hardcode


class Brain_monkey_logger(Brain_monkey_hardcode):
    def __init__(self, action_distance: float, logfile: str = None):
        super().__init__(memory_length=100, action_distance=action_distance)
        if logfile is not None:
            self.logfile = open(logfile, 'a+')

    def think(self, encoded_perception, encoded_messages):
        encoded_action, cause = super().think(encoded_perception=encoded_perception, encoded_messages=encoded_messages)

        logstring = encoded_perception + " " + encoded_messages + ""
        self.logfile.write(logstring)
        return encoded_action, cause
