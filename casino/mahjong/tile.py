from functools import total_ordering

from casino.core import SuitRankBase
from casino.exceptions import InvalidInstance
from casino.utils import add_metaclass


__all__ = ['Tile']


@add_metaclass(SuitRankBase)
@total_ordering
class Tile(object):

    SUIT_SPECIAL = 0
    SUIT_CHARACTER = 1
    SUIT_DOT = 2
    SUIT_BAMBOO = 3
    SUIT_WIND = 4
    SUIT_DRAGON = 5
    SUIT_FLOWER_RED = 6
    SUIT_FLOWER_BLACK = 7

    RANK_ONE = 1
    RANK_TWO = 2
    RANK_THREE = 3
    RANK_FOUR = 4
    RANK_FIVE = 5
    RANK_SIX = 6
    RANK_SEVEN = 7
    RANK_EIGHT = 8
    RANK_NINE = 9

    RANK_EAST = 10
    RANK_SOUTH = 11
    RANK_WEST = 12
    RANK_NORTH = 13

    RANK_RED = 14
    RANK_GREEN = 15
    RANK_WHITE = 16

    RANK_SPRING = 17
    RANK_SUMMER = 18
    RANK_AUTUMN = 19
    RANK_WINTER = 20

    RANK_PLUM = 21
    RANK_ORCHID = 22
    RANK_BAMBOO = 23
    RANK_CHRYSANTHEMUM = 24

    RANK_JOKER = 25

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.mask = (suit << 5) + rank

        self.suit_name = self.SUIT_NAMES.get(suit, 'invalid_suit')
        self.rank_name = self.RANK_NAMES.get(rank, 'invalid_rank')

        if not self.validate(suit, rank):
            raise InvalidInstance(str(self))

    @classmethod
    def _initialize_properties(cls):
        cls.NUMERIC_SUITS = (cls.SUIT_CHARACTER, cls.SUIT_DOT, cls.SUIT_BAMBOO)
        cls.NUMERIC_RANKS = (
            cls.RANK_ONE, cls.RANK_TWO, cls.RANK_THREE, cls.RANK_FOUR,
            cls.RANK_FIVE, cls.RANK_SIX, cls.RANK_SEVEN, cls.RANK_EIGHT,
            cls.RANK_NINE
        )
        cls.WIND_RANKS = (
            cls.RANK_EAST, cls.RANK_SOUTH, cls.RANK_WEST, cls.RANK_NORTH
        )
        cls.DRAGON_RANKS = (cls.RANK_RED, cls.RANK_GREEN, cls.RANK_WHITE)
        cls.FLOWER_RED_RANKS = (
            cls.RANK_SPRING, cls.RANK_SUMMER, cls.RANK_AUTUMN, cls.RANK_WINTER
        )
        cls.FLOWER_BLACK_RANKS = (
            cls.RANK_PLUM, cls.RANK_ORCHID, cls.RANK_BAMBOO,
            cls.RANK_CHRYSANTHEMUM
        )
        cls.SPECIAL_RANKS = (cls.RANK_JOKER,)

    @classmethod
    def _initialize_instances(cls):
        cls.CHARACTER_TILES = [
            cls(cls.SUIT_CHARACTER, rank) for rank in cls.NUMERIC_RANKS
        ]
        cls.DOT_TILES = [
            cls(cls.SUIT_DOT, rank) for rank in cls.NUMERIC_RANKS
        ]
        cls.BAMBOO_TILES = [
            cls(cls.SUIT_BAMBOO, rank) for rank in cls.NUMERIC_RANKS
        ]
        cls.NUMERIC_TILES = [
            cls(suit, rank)
            for suit in cls.NUMERIC_SUITS
            for rank in cls.NUMERIC_RANKS
        ]
        cls.WIND_TILES = [cls(cls.SUIT_WIND, rank) for rank in cls.WIND_RANKS]
        cls.DRAGON_TILES = [
            cls(cls.SUIT_DRAGON, rank) for rank in cls.DRAGON_RANKS
        ]
        cls.FLOWER_RED_TILES = [
            cls(cls.SUIT_FLOWER_RED, rank) for rank in cls.FLOWER_RED_RANKS
        ]
        cls.FLOWER_BLACK_TILES = [
            cls(cls.SUIT_FLOWER_BLACK, rank) for rank in cls.FLOWER_BLACK_RANKS
        ]
        cls.SPECIAL_TILES = [cls(cls.SUIT_SPECIAL, cls.RANK_JOKER)]

    @classmethod
    def create_tiles(cls, with_character=True, with_dot=True, with_bamboo=True,
                     with_wind=True, with_dragon=True,
                     with_flower_red=False, with_flower_black=False):
        tiles = []
        # tiles.extend(cls.NUMERIC_TILES)
        if with_character:
            tiles.extend(cls.CHARACTER_TILES)
        if with_dot:
            tiles.extend(cls.DOT_TILES)
        if with_bamboo:
            tiles.extend(cls.BAMBOO_TILES)
        if with_wind:
            tiles.extend(cls.WIND_TILES)
        if with_dragon:
            tiles.extend(cls.DRAGON_TILES)

        tiles = sorted(tiles * 4)
        if with_flower_red:
            tiles.extend(cls.FLOWER_RED_TILES)
        if with_flower_black:
            tiles.extend(cls.FLOWER_BLACK_TILES)
        return tiles

    @classmethod
    def validate(cls, suit, rank):
        return (
            (suit in cls.NUMERIC_SUITS and rank in cls.NUMERIC_RANKS) or
            (suit == cls.SUIT_WIND and rank in cls.WIND_RANKS) or
            (suit == cls.SUIT_DRAGON and rank in cls.DRAGON_RANKS) or
            (suit == cls.SUIT_SPECIAL and rank in cls.SPECIAL_RANKS) or
            (suit == cls.SUIT_FLOWER_RED and rank in cls.FLOWER_RED_RANKS) or
            (suit == cls.SUIT_FLOWER_BLACK and rank in cls.FLOWER_BLACK_RANKS)
        )

    @classmethod
    def validate_mask(cls, mask):
        return cls.validate((mask & 0xe0) >> 5, mask & 0x1f)

    @classmethod
    def from_mask(cls, mask):
        return Tile((mask & 0xe0) >> 5, mask & 0x1f)

    @classmethod
    def from_masks(cls, masks):
        return [Tile((mask & 0xe0) >> 5, mask & 0x1f) for mask in masks]

    def __add__(self, rank):
        # if not isinstance(rank, int):
        #     raise TypeError('cannot add Tile with %s' % type(rank))
        return Tile(self.suit, self.rank + rank)

    def __sub__(self, rank):
        # if not isinstance(rank, int):
        #     raise TypeError('cannot sub Tile with %s' % type(rank))
        return Tile(self.suit, self.rank - rank)

    def __eq__(self, other):
        # if not isinstance(other, Tile):
        #     return NotImplemented
        return self.mask == other.mask

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        # if not isinstance(other, Tile):
        #     return NotImplemented
        return self.mask < other.mask

    def __hash__(self):
        return self.mask

    def __str__(self):
        return '[{0},{1}]'.format(self.suit_name, self.rank_name)
    __repr__ = __unicode__ = __str__
