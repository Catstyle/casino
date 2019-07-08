from unittest import TestCase

from casino.mahjong import Tile, TileWall
from casino.mahjong.manager import MahjongManager


class MahjongTest(TestCase):

    def setUp(self):
        # 1w1w1w5w 1t2t4t7t 2T2T3T4T7T
        self.wall = TileWall.from_mask([
            33, 33, 33, 37, 65, 66, 68, 71, 98, 98, 99, 100, 103
        ])
        self.mahjong_manager = MahjongManager()
        self.mahjong_manager.has_pairs_patterns = True

    def test_wall(self):
        wall = self.wall
        self.assertEqual(wall.total_count, 13)
        self.assertDictEqual(wall.suits, {1: 4, 2: 4, 3: 5})
        self.assertDictEqual(
            wall.used_tiles,
            {'pong': [], 'chow': [],
             'kong': {'exposed': [], 'concealed': [], 'additional': []},
             'flower': []}
        )
        self.assertEqual(wall.available_count, 13)
        self.assertListEqual(wall.mask, [
            33, 33, 33, 37, 65, 66, 68, 71, 98, 98, 99, 100, 103
        ])

    def test_wall_add_tile(self):
        wall = self.wall
        tile = Tile.from_mask(35)
        self.assertNotIn(tile, wall.available_tiles)
        wall.add_tile(tile)
        self.assertEqual(wall.total_count, 14)
        self.assertEqual(wall.available_count, 14)
        self.assertIn(tile, wall.available_tiles)
        self.assertEqual(wall.suits[1], 5)

    def test_wall_remove_tile(self):
        wall = self.wall
        tile = Tile.from_mask(37)
        self.assertIn(tile, wall.available_tiles)
        wall.remove_tile(tile)
        self.assertNotIn(tile, wall.available_tiles)
        self.assertEqual(wall.total_count, 12)
        self.assertEqual(wall.available_count, 12)
        self.assertEqual(wall.suits[1], 3)

        with self.assertRaises(ValueError):
            wall.remove_tile(tile)

        tile = Tile.from_mask(33)
        self.assertIn(tile, wall.available_tiles)
        wall.remove_tile(tile)
        self.assertIn(tile, wall.available_tiles)
        self.assertEqual(wall.total_count, 11)
        self.assertEqual(wall.available_count, 11)
        self.assertEqual(wall.suits[1], 2)
