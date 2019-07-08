from __future__ import division

from functools import total_ordering

from casino.core import SuitRankBase
from casino.exceptions import InvalidInstance
from casino.utils import add_metaclass

__all__ = ['Card']


@add_metaclass(SuitRankBase)
@total_ordering
class Card(object):

    SUIT_DIAMOND = 1
    SUIT_CLUB = 2
    SUIT_HEART = 3
    SUIT_SPADE = 4
    SUIT_JOKER = 5
    SUIT_SPECIAL = 6

    RANK_THREE = 3
    RANK_FOUR = 4
    RANK_FIVE = 5
    RANK_SIX = 6
    RANK_SEVEN = 7
    RANK_EIGHT = 8
    RANK_NINE = 9
    RANK_TEN = 10
    RANK_JACK = 11
    RANK_QUEEN = 12
    RANK_KING = 13
    RANK_ACE = 14
    RANK_TWO = 16
    RANK_BLACK = 20
    RANK_RED = 21

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.mask = suit * 100 + rank

        self.suit_name = self.SUIT_NAMES.get(suit, suit)
        self.rank_name = self.RANK_NAMES.get(rank, rank)

        if not self.validate(suit, rank):
            raise InvalidInstance(str(self))

    @classmethod
    def _initialize_properties(cls):
        cls.NORMAL_SUITS = (
            cls.SUIT_DIAMOND, cls.SUIT_CLUB, cls.SUIT_HEART, cls.SUIT_SPADE
        )
        cls.NORMAL_RANKS = tuple(sorted([
            cls.RANK_ACE, cls.RANK_TWO, cls.RANK_THREE, cls.RANK_FOUR,
            cls.RANK_FIVE, cls.RANK_SIX, cls.RANK_SEVEN, cls.RANK_EIGHT,
            cls.RANK_NINE, cls.RANK_TEN, cls.RANK_JACK, cls.RANK_QUEEN,
            cls.RANK_KING,
        ]))
        cls.JOKER_RANKS = (cls.RANK_BLACK, cls.RANK_RED)

    @classmethod
    def _initialize_instances(cls):
        cls.NORMAL_CARDS = [
            cls(suit, rank)
            for suit in cls.NORMAL_SUITS
            for rank in cls.NORMAL_RANKS
        ]
        cls.NORMAL_CARDS.sort()
        cls.JOKER_CARDS = [
            cls(cls.SUIT_JOKER, cls.RANK_BLACK),
            cls(cls.SUIT_JOKER, cls.RANK_RED),
        ]

    @classmethod
    def create_cards(cls, with_joker=True):
        cards = []
        cards.extend(cls.NORMAL_CARDS)
        if with_joker:
            cards.extend(cls.JOKER_CARDS)
        return cards

    @classmethod
    def validate(cls, suit, rank):
        return (
            (suit in cls.NORMAL_SUITS and rank in cls.NORMAL_RANKS) or
            (suit == cls.SUIT_JOKER and rank in cls.JOKER_RANKS) or
            suit == cls.SUIT_SPECIAL
        )

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
        # if not isinstance(rank, int):
        #     raise TypeError('cannot add Card with %s' % type(rank))
        return Card(self.suit, self.rank + rank)

    def __sub__(self, rank):
        # if not isinstance(rank, int):
        #     raise TypeError('cannot sub Card with %s' % type(rank))
        return Card(self.suit, self.rank - rank)

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return (
            self.rank < other.rank or
            (self.rank == other.rank and self.suit < other.suit)
        )

    def __hash__(self):
        return self.mask

    def __str__(self):
        return '[{},{}]'.format(self.suit_name, self.rank_name)
    __repr__ = __unicode__ = __str__
