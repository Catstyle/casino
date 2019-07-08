from bisect import insort
from collections import Counter

from .tile import Tile

__all__ = ['TileWall']


class TileWall(object):

    def __init__(self, tiles):
        self.available_tiles = sorted(tiles)
        self.used_tiles = {
            'pong': [],
            'chow': [],
            'kong': {'exposed': [], 'concealed': [], 'additional': []},
            'flower': []
        }
        self.used_count = 0
        suits = self.suits = Counter()
        for tile in self.available_tiles:
            suits[tile.suit] += 1

    @classmethod
    def from_mask(cls, masks):
        return cls(Tile.from_mask(mask) for mask in masks)

    @property
    def mask(self):
        return [tile.mask for tile in self.all_tiles]

    @property
    def total_count(self):
        return len(self.available_tiles) + self.used_count

    @property
    def available_count(self):
        return len(self.available_tiles)

    @property
    def all_tiles(self):
        used_tiles = self.used_tiles
        return sorted(
            self.available_tiles +
            sum(used_tiles['pong'], []) + sum(used_tiles['chow'], []) +
            sum(sum(used_tiles['kong'].values(), []), [])
        )

    def add_tile(self, tile):
        insort(self.available_tiles, tile)
        self.suits[tile.suit] += 1

    def remove_tile(self, tile):
        self.available_tiles.remove(tile)
        self.suits[tile.suit] -= 1

    def __str__(self):
        return '[available_tiles|%s][used_tiles|%s]' % (
            self.available_tiles, self.used_tiles,
        )
    __unicode__ = __repr__ = __str__
