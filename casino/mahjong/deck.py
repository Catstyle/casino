__all__ = ['Deck']


class Deck(object):

    def __init__(self, tiles):
        self.tiles = tiles
        self.tile_set = set(tiles)
        self.suits = {tile.suit for tile in tiles}

    def exclude_rank(self, exclude_ranks):
        self.tiles = [tile for tile in self.tiles
                      if tile.rank not in exclude_ranks]
        return self

    def exclude_suit(self, exclude_suits):
        self.tiles = [tile for tile in self.tiles
                      if tile.suit not in exclude_suits]
        return self

    def sort(self):
        self.tiles.sort()

    def __getitem__(self, index):
        return self.tiles[index]

    def __len__(self):
        return len(self.tiles)

    def __getslice__(self, begin, end):
        return self.tiles[begin:end]

    def __contains__(self, tile):
        return tile in self.tiles

    def __str__(self):
        return '|'.join([str(tile) for tile in self.tiles])
    __unicode__ = __repr__ = __str__
