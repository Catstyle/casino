from casino.core import PatternMeta
from casino.utils import add_metaclass


@add_metaclass(PatternMeta)
class BasePattern(object):

    id = None
    priority = 0
    POINT = 0

    @staticmethod
    def validate(tile_wall, combinations, properties):
        raise NotImplementedError()


class BasePairs(BasePattern):
    pass


class Normal(BasePattern):

    id = 1001
    priority = 0
    POINT = 0

    @staticmethod
    def validate(tile_wall, combinations, properties):
        tile_wall.used_combs[:] = combinations
        return bool(combinations)


class Pairs(BasePairs):

    id = 1002
    priority = 1
    POINT = 0

    @staticmethod
    def validate(tile_wall, combinations, properties):
        return properties.pairs
