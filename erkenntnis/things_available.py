from .thing import Thing


class Stone(Thing):
    def __init__(self, position, velocity=None, radius=None):
        super().__init__(position=position, velocity=velocity, radius=radius)
        self.type_properties = "stone"     # could be equivalent to encoding of size of sheep, fur of wolf, number of limbs, ...


class Grass(Thing):
    def __init__(self, position, velocity=None, radius=None):
        super().__init__(position=position, velocity=velocity, radius=radius)
        self.type_properties = "grass"     # could be equivalent to encoding of size of sheep, fur of wolf, number of limbs, ...


class Mirror(Thing):
    def __init__(self, position, velocity=None, radius=None):
        super().__init__(position=position, velocity=velocity, radius=radius)
        self.type_properties = "mirror"     # could be equivalent to encoding of size of sheep, fur of wolf, number of limbs, ...
