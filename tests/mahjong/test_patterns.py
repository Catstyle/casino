from unittest import TestCase

from casino.mahjong import Tile, TileWall
from casino.mahjong.patterns import Pairs, Normal
from casino.mahjong.manager import MahjongManager


class PatternTest(TestCase):

    def setUp(self):
        self.mahjong_manager = MahjongManager()
        self.mahjong_manager.register_patterns([Pairs, Normal])

    def test_7_pairs(self):
        mm = self.mahjong_manager
        # 1w1w 2w2w 3w3w 6w6w 8w8w 9w9w 9t
        wall = TileWall.from_mask([
            33, 33, 34, 34, 35, 35, 38, 38, 40, 40, 41, 41, 73
        ])
        tile = Tile.from_mask(73)
        self.assertTrue(mm.check_win_by_tile(wall.available_tiles, tile))
        self.assertIs(mm.get_pattern_by_tile(wall, tile), Pairs)

    def test_normal(self):
        mm = self.mahjong_manager
        # 1w2w3w 4w4w 6t7t8t 9t9t9t 7T7T
        wall = TileWall.from_mask([
            33, 34, 35, 36, 36, 70, 71, 72, 73, 73, 73, 103, 103
        ])
        tile = Tile.from_mask(36)
        self.assertIs(mm.get_pattern_by_tile(wall, tile), Normal)

        tile2 = Tile.from_mask(103)
        self.assertIs(mm.get_pattern_by_tile(wall, tile2), Normal)
