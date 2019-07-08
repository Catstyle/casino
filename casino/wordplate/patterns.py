from casino.core import PatternMeta
from casino.utils import add_metaclass


@add_metaclass(PatternMeta)
class Normal(object):

    id = 1001
    POINT = 0

    @staticmethod
    def validate(handcard, combinations, properties):
        if not (combinations or handcard.fixed_cards):
            return False

        handcard.used_combs[:] = combinations
        return True


patterns = (Normal,)
