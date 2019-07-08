from unittest import TestCase

from casino.exceptions import InvalidInstance
from casino.mahjong import Tile


class TileTest(TestCase):

    def test_tile_suits(self):
        self.assertTupleEqual(Tile.NUMERIC_SUITS, (1, 2, 3))
        self.assertTupleEqual(Tile.SUITS, (0, 1, 2, 3, 4, 5, 6, 7))

    def test_tile_ranks(self):
        self.assertTupleEqual(Tile.NUMERIC_RANKS, (1, 2, 3, 4, 5, 6, 7, 8, 9))
        self.assertTupleEqual(Tile.WIND_RANKS, (10, 11, 12, 13))
        self.assertTupleEqual(Tile.DRAGON_RANKS, (14, 15, 16))
        self.assertTupleEqual(Tile.FLOWER_RED_RANKS, (17, 18, 19, 20))
        self.assertTupleEqual(Tile.FLOWER_BLACK_RANKS, (21, 22, 23, 24))
        self.assertTupleEqual(Tile.SPECIAL_RANKS, (25,))

    def test_invalid_tile(self):
        with self.assertRaises(InvalidInstance):
            Tile.from_mask(1)
        with self.assertRaises(InvalidInstance):
            Tile(10, 10)

    def test_tile_mask(self):
        tile = Tile(Tile.SUIT_BAMBOO, Tile.RANK_ONE)
        self.assertEqual(tile.mask, 97)
        self.assertEqual(Tile.from_mask(97), tile)

    def test_tile_masks(self):
        tile = Tile(Tile.SUIT_BAMBOO, Tile.RANK_ONE)
        tile2 = Tile(Tile.SUIT_BAMBOO, Tile.RANK_TWO)
        self.assertListEqual(Tile.from_masks([97, 98]), [tile, tile2])

    def test_tile_str(self):
        tile = Tile(Tile.SUIT_BAMBOO, Tile.RANK_ONE)
        self.assertEqual(str(tile), '[BAMBOO,ONE]')

    def test_tile_sort_order(self):
        # 4w, 2w, 7w
        tiles = [Tile.from_mask(36), Tile.from_mask(34), Tile.from_mask(39)]
        tiles.sort()
        self.assertListEqual([tile.mask for tile in tiles], [34, 36, 39])

    def test_tile_add(self):
        tile = Tile(Tile.SUIT_BAMBOO, Tile.RANK_ONE)
        self.assertEqual(tile + 1, Tile(Tile.SUIT_BAMBOO, Tile.RANK_TWO))

    def test_tile_invalid_add(self):
        tile = Tile(Tile.SUIT_BAMBOO, Tile.RANK_ONE)
        with self.assertRaises(InvalidInstance):
            tile + 9
        with self.assertRaises(TypeError):
            tile + '1'

    def test_tile_eq(self):
        self.assertEqual(Tile.from_mask(33), Tile.from_mask(33))
        self.assertEqual(Tile.from_mask(33), Tile(1, 1))

    def test_tile_lt(self):
        self.assertLessEqual(Tile.from_mask(33), Tile.from_mask(34))

    def test_tile_hashable(self):
        tile_set = set([Tile.from_mask(33), Tile.from_mask(33)])
        self.assertEqual(len(tile_set), 1)
        self.assertIn(Tile.from_mask(33), tile_set)
        self.assertNotIn(Tile.from_mask(34), tile_set)
