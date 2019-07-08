from functools import total_ordering

from casino.core import SuitRankBase
from casino.exceptions import InvalidInstance
from casino.utils import add_metaclass


@add_metaclass(SuitRankBase)
@total_ordering
class Card(object):

    SUIT_LOWER = 1
    SUIT_UPPER = 2

    RANK_ONE = 1
    RANK_TWO = 2
    RANK_THREE = 3
    RANK_FOUR = 4
    RANK_FIVE = 5
    RANK_SIX = 6
    RANK_SEVEN = 7
    RANK_EIGHT = 8
    RANK_NINE = 9
    RANK_TEN = 10

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.mask = suit * 100 + rank

        self.suit_name = self.SUIT_NAMES.get(suit, 'invalid_suit')
        self.rank_name = self.RANK_NAMES.get(rank, 'invalid_rank')

        if not self.validate(suit, rank):
            raise InvalidInstance(str(self))

    @classmethod
    def _initialize_properties(cls):
        pass

    @classmethod
    def _initialize_instances(cls):
        cls.NORMAL_CARDS = [
            cls(suit, rank)
            for suit in cls.SUITS
            for rank in cls.RANKS
        ]
        cls.RED_CARDS = [
            cls(suit, rank)
            for suit in cls.SUITS
            for rank in (cls.RANK_TWO, cls.RANK_SEVEN, cls.RANK_TEN)
        ]

    @classmethod
    def validate(cls, suit, rank):
        return suit in cls.SUITS and rank in cls.RANKS

    @classmethod
    def validate_mask(cls, mask):
        return cls.validate(mask // 100, mask % 100)

    @classmethod
    def from_mask(cls, mask):
        return cls(mask // 100, mask % 100)

    @classmethod
    def from_masks(cls, masks):
        return [cls(mask // 100, mask % 100) for mask in masks]

    def __add__(self, rank):
        return self.__class__(self.suit, self.rank + rank)

    def __sub__(self, rank):
        return self.__class__(self.suit, self.rank - rank)

    def __eq__(self, other):
        return self.mask == other.mask

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.mask < other.mask

    def __invert__(self):
        """return the instance of logical negation"""
        if self.suit == self.SUIT_LOWER:
            return self.__class__(self.SUIT_UPPER, self.rank)
        elif self.suit == self.SUIT_UPPER:
            return self.__class__(self.SUIT_LOWER, self.rank)
        assert False, ('unknown suit', self)

    def __hash__(self):
        return self.mask

    def __str__(self):
        return '[{},{}]'.format(self.suit_name, self.rank_name)
    __repr__ = __unicode__ = __str__
