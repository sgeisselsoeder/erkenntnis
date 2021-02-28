from .thing import thing


class wall(thing):
    def __init__(self, position, velocity=None):
        super().__init__(position=position, velocity=velocity)
        self.type_properties = "wall"     # could be equivalent to encoding of size of sheep, fur of wolf, number of limbs, ...
