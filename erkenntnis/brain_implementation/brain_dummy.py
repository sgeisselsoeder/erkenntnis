from .brain_simple_memory import Brain_simple_memory


class Brain_dummy(Brain_simple_memory):
    def __init__(self, logfile: str = None):
        super().__init__(memory_length=1, logfile=logfile)
