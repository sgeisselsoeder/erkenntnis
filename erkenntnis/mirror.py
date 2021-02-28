from .thing import thing


class mirror(thing):
    def __init__(self, position, velocity=None):
        super().__init__(position=position, velocity=velocity)
        self.type_properties = "mirror"     # could be equivalent to encoding of size of sheep, fur of wolf, number of limbs, ...
