from .thing import Thing


class Stone(Thing):
    def __init__(self, position, velocity=None, radius=None):
        super().__init__(position=position, velocity=velocity, radius=radius)
        self.type_properties = "stone"


def get_stone(position, velocity=None, radius=None):
    return Stone(position=position, velocity=velocity, radius=radius)


class Grass(Thing):
    def __init__(self, position, velocity=None, radius=None):
        super().__init__(position=position, velocity=velocity, radius=radius)
        self.type_properties = "grass"


def get_grass(position, velocity=None, radius=None):
    return Grass(position=position, velocity=velocity, radius=radius)


class Mirror(Thing):
    def __init__(self, position, velocity=None, radius=None):
        super().__init__(position=position, velocity=velocity, radius=radius)
        self.type_properties = "mirror"


def get_mirror(position, velocity=None, radius=None):
    return Mirror(position=position, velocity=velocity, radius=radius)
