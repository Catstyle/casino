import random
from unittest import TestCase

from casino.mahjong import Tile, TileWall
from casino.mahjong.deck import Deck
from casino.mahjong.manager import MahjongManager
from casino.mahjong.patterns import Pairs, Normal
from casino.mahjong.properties import combinations


class MahjongTest(TestCase):

    def setUp(self):
        self.deck = Deck(Tile.create_tiles())
        self.mahjong_manager = MahjongManager()
        self.mahjong_manager.reset(self.deck, random)
        self.wall = TileWall.from_mask([
            33, 33, 33, 37, 38, 39, 66, 68, 98, 98, 99, 100, 101,
        ])

    def test_reset_with_joker_factory(self):
        manager = self.mahjong_manager

        def func(deck):
            return Tile.from_mask(33), {Tile.from_mask(33)}
        manager.set_joker_factory(func)
        manager.reset(self.deck, random)
        self.assertEqual(manager.jokers, {Tile.from_mask(33)})

    def test_left_tiles(self):
        self.assertEqual(len(self.deck), self.mahjong_manager.left_tiles)

    def test_has_pairs_patterns(self):
        self.assertFalse(self.mahjong_manager.has_pairs_patterns)
        self.mahjong_manager.register_pattern(Pairs)
        self.assertTrue(self.mahjong_manager.has_pairs_patterns)

    def test_register_patterns(self):
        manager = self.mahjong_manager
        manager.register_patterns([Normal, Pairs])
        self.assertListEqual(manager.patterns, [Pairs, Normal])

    def test_pong_tile(self):
        mm = self.mahjong_manager
        wall = self.wall
        tile = Tile.from_mask(98)
        self.assertTrue(mm.check_pong_tile(wall, tile))
        self.assertEqual(wall.available_tiles.count(tile), 2)
        self.assertNotIn(tile, wall.used_tiles['pong'])

        mm.pong(wall, tile)
        self.assertEqual(wall.available_tiles.count(tile), 0)
        self.assertIn([tile, tile, tile], wall.used_tiles['pong'])
        self.assertEqual(wall.available_count, 11)

        self.assertFalse(mm.check_pong_tile(wall, Tile.from_mask(37)))

    def test_exposed_kong(self):
        mm = self.mahjong_manager
        wall = self.wall
        tile = Tile.from_mask(33)
        self.assertTrue(mm.check_exposed_kong(wall, tile))
        self.assertEqual(wall.available_tiles.count(tile), 3)
        self.assertNotIn(tile, wall.used_tiles['kong'])

        mm.exposed_kong(wall, tile)
        self.assertEqual(wall.available_tiles.count(tile), 0)
        self.assertIn(
            [tile, tile, tile, tile], wall.used_tiles['kong']['exposed']
        )
        self.assertEqual(wall.available_count, 10)

    def test_concealed_kong(self):
        mm = self.mahjong_manager
        wall = self.wall
        tile = Tile.from_mask(33)
        self.assertListEqual(mm.get_concealed_kong_tiles(wall), [])

        wall.add_tile(tile)
        self.assertTrue(mm.check_concealed_kong(wall, tile))
        self.assertListEqual(mm.get_concealed_kong_tiles(wall), [tile])
        mm.concealed_kong(wall, tile)

        self.assertEqual(wall.available_tiles.count(tile), 0)
        self.assertIn(
            [tile, tile, tile, tile], wall.used_tiles['kong']['concealed']
        )
        self.assertEqual(wall.available_count, 10)

    def test_additional_kong(self):
        mm = self.mahjong_manager
        wall = self.wall
        tile = Tile.from_mask(98)
        mm.pong(wall, tile)
        self.assertIn([tile, tile, tile], wall.used_tiles['pong'])

        self.assertListEqual(mm.get_additional_kong_tiles(wall), [])
        wall.add_tile(tile)
        self.assertTrue(mm.check_additional_kong(wall, tile))
        self.assertListEqual(mm.get_additional_kong_tiles(wall), [tile])
        mm.additional_kong(wall, tile)
        self.assertNotIn([tile, tile, tile], wall.used_tiles['pong'])
        self.assertIn(
            [tile, tile, tile, tile], wall.used_tiles['kong']['additional']
        )
        self.assertEqual(wall.available_count, 11)

    def test_wall_actions(self):
        # 1w2w2w4w5w8w 5t6t6t 1T6T7T7T
        wall = TileWall.from_mask([
            33, 34, 34, 36, 37, 40, 69, 70, 70, 97, 102, 103, 103
        ])
        self.assertEqual(wall.used_count, 0)
        self.assertEqual(wall.available_count, 13)

        # drawn 2w
        wall.add_tile(Tile.from_mask(34))
        # discard 1T
        wall.remove_tile(Tile.from_mask(97))

        mm = self.mahjong_manager
        # pong 6t
        t6 = Tile.from_mask(70)
        mm.pong(wall, t6)
        # discard 5t
        wall.remove_tile(Tile.from_mask(69))
        self.assertDictEqual(
            wall.used_tiles,
            {'kong': {'exposed': [], 'concealed': [], 'additional': []},
             'chow': [], 'pong': [[t6, t6, t6]],
             'flower': []}
        )

        # drawn 8w
        wall.add_tile(Tile.from_mask(40))
        # discard 1w
        wall.remove_tile(Tile.from_mask(33))

        # pong 7T
        T7 = Tile.from_mask(103)
        mm.pong(wall, T7)
        # discard 6T
        wall.remove_tile(Tile.from_mask(102))
        self.assertDictEqual(
            wall.used_tiles,
            {'kong': {'exposed': [], 'concealed': [], 'additional': []},
             'chow': [], 'pong': [[t6, t6, t6], [T7, T7, T7]],
             'flower': []}
        )

        w3 = Tile.from_mask(35)
        self.assertTrue(mm.check_win_by_tile(wall.available_tiles, w3))

    def test_chow_tile(self):
        mm = self.mahjong_manager
        wall = self.wall
        dot3 = Tile(2, 3)
        self.assertTrue(mm.check_chow_tile(wall, dot3))
        self.assertFalse(mm.check_chow_tile(wall, Tile(2, 5)))

        self.assertTrue(mm.check_chow_tiles([Tile(2, 1), Tile(2, 2)], dot3))
        self.assertTrue(mm.check_chow_tiles([Tile(2, 2), Tile(2, 4)], dot3))
        self.assertFalse(mm.check_chow_tiles([Tile(2, 1), Tile(2, 4)], dot3))
        mm.chow(wall, [Tile(2, 2), Tile(2, 4)], dot3)
        self.assertListEqual(
            wall.used_tiles['chow'], [[Tile(2, 2), dot3, Tile(2, 4)]]
        )

        self.assertFalse(mm.check_chow_tiles([], dot3))

    def test_get_combinations(self):
        tiles = Tile.from_masks([33, 34, 35, 38, 38, 38, 71, 71])
        self.assertListEqual(
            list(combinations(tiles)),
            list(self.mahjong_manager.get_combinations(tiles))
        )

        tiles = Tile.from_masks([33, 34, 35, 36, 38, 38, 38])
        self.assertListEqual(
            list(combinations(tiles, 1)),
            list(self.mahjong_manager.get_combinations(tiles, 1))
        )

    def test_get_pattern(self):
        manager = self.mahjong_manager
        manager.register_patterns([Pairs, Normal])
        wall = TileWall.from_mask([33, 34, 35, 36, 36, 38, 38, 38])
        self.assertEqual(manager.get_pattern(wall), Normal)

        wall = TileWall.from_mask([
            33, 33, 34, 34, 35, 35, 38, 38, 39, 39, 40, 40, 41, 41
        ])
        self.assertEqual(manager.get_pattern(wall), Pairs)

    def test_get_pattern_by_tile(self):
        manager = self.mahjong_manager
        manager.register_patterns([Pairs, Normal])
        wall = TileWall.from_mask([33, 34, 35, 36, 38, 38, 38])
        self.assertEqual(
            manager.get_pattern_by_tile(wall, Tile.from_mask(36)), Normal
        )

        wall = TileWall.from_mask([
            33, 33, 34, 34, 35, 35, 38, 38, 39, 39, 40, 40, 41
        ])
        self.assertEqual(
            manager.get_pattern_by_tile(wall, Tile.from_mask(41)), Pairs
        )

    def test_get_pattern_with_joker(self):
        manager = self.mahjong_manager
        manager.register_patterns([Pairs, Normal])

        def func(deck):
            return Tile.from_mask(33), {Tile.from_mask(33)}
        manager.set_joker_factory(func)
        wall = TileWall.from_mask([33, 34, 35, 36, 36, 38, 38, 38])
        self.assertEqual(manager.get_pattern(wall), Normal)

        wall = TileWall.from_mask([
            33, 33, 34, 34, 35, 35, 38, 38, 39, 39, 40, 40, 41, 41
        ])
        self.assertEqual(manager.get_pattern(wall), Pairs)

    def test_get_pattern_by_tile_with_joker(self):
        manager = self.mahjong_manager
        manager.register_patterns([Pairs, Normal])

        def func(deck):
            return Tile.from_mask(33), {Tile.from_mask(33)}
        manager.set_joker_factory(func)
        wall = TileWall.from_mask([33, 34, 35, 36, 38, 38, 38])
        self.assertEqual(
            manager.get_pattern_by_tile(wall, Tile.from_mask(36)), Normal
        )

        wall = TileWall.from_mask([
            33, 33, 34, 34, 35, 35, 38, 38, 39, 39, 40, 40, 41
        ])
        self.assertEqual(
            manager.get_pattern_by_tile(wall, Tile.from_mask(41)), Pairs
        )

    def test_get_candidates(self):
        manager = self.mahjong_manager
        tiles = Tile.from_masks([33, 34, 35, 36, 38, 38, 38])
        self.assertEqual(
            list(manager.get_candidates(tiles)), Tile.from_masks([33, 36, 37])
        )

        tiles = Tile.from_masks([
            33, 33, 33, 34, 35, 36, 37, 38, 39, 40, 41, 41, 41
        ])
        self.assertEqual(
            list(manager.get_candidates(tiles)), Tile.from_masks(range(33, 42))
        )

        tiles = Tile.from_masks([33, 34, 35, 38, 38, 38])
        self.assertEqual(list(manager.get_candidates(tiles)), [])

        # pairs
        manager.has_pairs_patterns = True
        tiles = Tile.from_masks([
            33, 33, 34, 34, 35, 35, 36, 36, 66, 66, 68, 68, 99
        ])
        self.assertEqual(
            list(manager.get_candidates(tiles)), [Tile.from_mask(99)]
        )

        tiles = Tile.from_masks([
            66, 66, 67, 67, 68, 68, 69, 70, 70, 71, 71, 73, 73
        ])
        self.assertEqual(
            sorted(manager.get_candidates(tiles)),
            [Tile.from_mask(69), Tile.from_mask(72)]
        )

        manager._use_joker_api()
        manager.jokers = {Tile(1, 5)}
        tiles = Tile.from_masks([
            33, 33, 34, 34, 35, 35, 37, 37, 66, 66, 68, 68, 99
        ])
        self.assertEqual(
            sorted(manager.get_candidates(tiles)),
            sorted(manager.deck.tile_set)
        )

        manager.jokers = {Tile.DRAGON_RED}
        tiles = Tile.from_masks([
            36, 37, 37, 38, 38, 39, 39, 40, 40, 41, 41, 65, 65
        ])
        self.assertEqual(
            sorted(manager.get_candidates(tiles)),
            [Tile.CHARACTER_FOUR, Tile.CHARACTER_SEVEN],
        )

    def test_has_candidates(self):
        manager = self.mahjong_manager
        tiles = Tile.from_masks([33, 34, 35, 36, 38, 38, 38])
        self.assertTrue(manager.has_candidates(tiles))

        tiles = Tile.from_masks([33, 34, 35, 38, 38, 38])
        self.assertFalse(manager.has_candidates(tiles))

        tiles = Tile.from_masks([
            33, 33, 34, 34, 36, 36, 65, 65, 67, 67, 99, 103, 103
        ])
        manager.has_pairs_patterns = True
        self.assertTrue(manager.has_candidates(tiles))

    def test_get_candidates_with_joker(self):
        mm = self.mahjong_manager
        mm._use_joker_api()
        mm.jokers = {Tile(1, 5)}
        tiles = Tile.from_masks([33, 37, 37, 38, 38, 71, 71])
        self.assertListEqual(
            list(mm.get_candidates(tiles)),
            Tile.from_masks([33, 34, 35, 38, 71])
        )

        tiles = Tile.from_masks([
            33, 33, 37, 37, 37, 37, 38, 38, 71, 71, 72, 72, 73
        ])
        self.assertListEqual(
            sorted(mm.get_candidates(tiles)), sorted(mm.deck.tile_set)
        )

    def test_has_candidates_with_joker(self):
        mm = self.mahjong_manager
        mm._use_joker_api()
        mm.jokers = {Tile(1, 5)}
        tiles = Tile.from_masks([33, 37, 37, 38, 38, 71, 71])
        self.assertTrue(mm.has_candidates(tiles))

        tiles = Tile.from_masks([
            33, 33, 37, 37, 37, 37, 38, 38, 71, 71, 72, 72, 73
        ])
        self.assertTrue(mm.has_candidates(tiles))

        tiles = Tile.from_masks([
            33, 33, 34, 34, 36, 36, 37, 65, 65, 67, 99, 103, 103
        ])
        mm.has_pairs_patterns = True
        self.assertTrue(mm.has_candidates(tiles))

    def test_check_win(self):
        mm = self.mahjong_manager
        tiles = Tile.from_masks([
            33, 33, 37, 37, 38, 38, 39, 39, 70, 71, 71, 72, 72, 73
        ])
        self.assertTrue(mm.check_win(tiles))

        tiles = Tile.from_masks([
            33, 33, 37, 37, 38, 38, 39, 39, 70, 71, 71, 72, 72, 73, 73
        ])
        self.assertFalse(mm.check_win(tiles))

        tiles = Tile.from_masks([
            33, 33, 37, 37, 38, 38, 39, 39, 70, 71, 71, 72, 72
        ])
        self.assertFalse(mm.check_win(tiles))

    def test_check_win_with_joker(self):
        mm = self.mahjong_manager
        mm._use_joker_api()
        joker = Tile.from_mask(37)
        tiles = Tile.from_masks([33, 34, 37, 37, 38, 38, 71, 71])
        mm.jokers = set([joker])
        self.assertTrue(mm.check_win(tiles))

        joker = Tile.from_mask(141)
        tiles = Tile.from_masks([36, 38, 39, 40, 41, 68, 141, 141])
        mm.jokers = set([joker])
        self.assertTrue(mm.check_win(tiles))

        joker = Tile.from_mask(99)
        mm.jokers = set([joker])
        tiles = Tile.from_masks([36, 38, 40, 41, 68, 99, 99, 99])
        self.assertTrue(mm.check_win(tiles))

        tiles = Tile.from_masks([39, 40, 41, 138, 139, 99, 99, 99])
        self.assertTrue(mm.check_win(tiles))

        tiles = Tile.from_masks([34, 35, 35, 36, 36, 36, 37, 37, 38, 138, 99])
        self.assertTrue(mm.check_win(tiles))

        tiles = Tile.from_masks([34, 34, 36, 37, 38, 138, 99, 99])
        self.assertTrue(mm.check_win(tiles))

        joker = Tile.from_mask(67)
        mm.jokers = set([joker])
        tiles = Tile.from_masks([
            35, 36, 37, 67, 68, 68, 69, 70, 71, 102, 102, 103, 104, 105
        ])
        self.assertTrue(mm.check_win(tiles))

        tiles = Tile.from_masks([
            33, 33, 37, 37, 38, 38, 39, 39, 70, 71, 71, 72, 72, 73, 73
        ])
        self.assertFalse(mm.check_win(tiles))

        tiles = Tile.from_masks([
            33, 33, 37, 37, 38, 38, 39, 39, 70, 71, 71, 72, 72
        ])
        self.assertFalse(mm.check_win(tiles))

    def test_has_free_joker(self):
        mm = self.mahjong_manager
        mm._use_joker_api()
        joker = Tile.from_mask(37)
        mm.jokers = set([joker])

        tiles = Tile.from_masks([33, 34, 35, 38, 38, 71, 71])
        self.assertFalse(mm.has_free_joker(tiles))

        tiles = Tile.from_masks([33, 34, 35, 37, 71, 71, 71])
        self.assertTrue(mm.has_free_joker(tiles))

        tiles = Tile.from_masks([33, 34, 37, 37, 71, 71, 71])
        self.assertTrue(mm.has_free_joker(tiles))

        tiles = Tile.from_masks([33, 34, 37, 38, 71, 71, 71])
        self.assertFalse(mm.has_free_joker(tiles))

        tiles = Tile.from_masks([37, 37, 71, 71, 71, 97, 98])
        self.assertTrue(mm.has_free_joker(tiles))

        tiles = Tile.from_masks([37, 37, 37, 71, 71, 97, 103])
        self.assertFalse(mm.has_free_joker(tiles))
