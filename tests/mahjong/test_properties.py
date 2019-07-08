from unittest import TestCase

from casino.mahjong import Tile
from casino.mahjong.properties import (
    is_same_suit, is_7_pairs, is_7_pairs_with_joker, get_lack_of_joker,
    combinations
)


class PropertiesTest(TestCase):

    def test_is_same_suit(self):
        tiles = Tile.from_masks([
            33, 33, 37, 37, 38, 38, 39, 39, 39, 39, 40, 40, 41, 41
        ])
        self.assertTrue(is_same_suit(tiles))

        tiles = Tile.from_masks([
            33, 33, 37, 37, 38, 38, 71, 71, 73, 73, 97, 97, 98, 98
        ])
        self.assertFalse(is_same_suit(tiles))

    def test_is_7_pairs(self):
        tiles = Tile.from_masks([
            33, 33, 37, 37, 38, 38, 71, 71, 73, 73, 97, 97, 98, 98
        ])
        self.assertTrue(is_7_pairs(tiles))

        tiles = Tile.from_masks([
            33, 33, 34, 34, 35, 35, 36, 36, 38, 39, 65, 65, 65, 65
        ])
        self.assertFalse(is_7_pairs(tiles))

    def test_is_7_pairs_with_joker(self):
        tiles = Tile.from_masks([
            33, 33, 34, 34, 35, 35, 36, 36, 38, 39, 65, 65, 65, 65
        ])
        for joker, count in ((Tile.from_mask(65), 4), (Tile.from_mask(38), 1),
                             (Tile.from_mask(39), 1), (Tile.from_mask(34), 2)):
            self.assertTrue(is_7_pairs_with_joker(
                [tile for tile in tiles if tile is not joker], count
            ))

        tiles = Tile.from_masks([
            33, 33, 34, 34, 35, 35, 36, 36, 37, 38, 39, 65, 65, 65
        ])
        self.assertTrue(is_7_pairs_with_joker(
            [tile for tile in tiles if tile is not Tile.from_mask(65)], 3
        ))

    def test_get_lack_of_joker(self):
        tiles = Tile.from_masks([33, 34, 35, 36, 38, 38, 38])
        self.assertEqual(get_lack_of_joker(tiles), 2)

        tiles = Tile.from_masks([33, 36, 38, 38, 38])
        self.assertEqual(get_lack_of_joker(tiles), 4)

        tiles = Tile.from_masks([33, 33, 33, 36, 38, 39])
        self.assertEqual(get_lack_of_joker(tiles), 3)

        tiles = Tile.from_masks([33, 33, 33, 138, 138])
        self.assertEqual(get_lack_of_joker(tiles), 1)

        tiles = Tile.from_masks([33, 33, 33])
        self.assertEqual(get_lack_of_joker(tiles), 0)

        tiles = Tile.from_masks([])
        self.assertEqual(get_lack_of_joker(tiles), 0)

    def test_combinations(self):
        tiles = Tile.from_masks([33, 34, 35, 38, 38, 38, 71, 71])
        self.assertListEqual(
            list(combinations(tiles)),
            [{
                'triplets': [Tile.from_masks([38, 38, 38])],
                'sequences':[Tile.from_masks([33, 34, 35])],
                'eye': Tile.from_masks([71, 71]),
                'joker_count': 0,
            }]
        )

        tiles = Tile.from_masks([33, 34, 35, 38, 38, 38, 71])
        self.assertListEqual(list(combinations(tiles)), [])

        tiles = Tile.from_masks([33, 34, 35, 36, 38, 38, 38])
        self.assertListEqual(
            list(combinations(tiles, 1)),
            [
                {
                    'triplets': [Tile.from_masks([38, 38, 38])],
                    'sequences':[Tile.from_masks([34, 35, 36])],
                    'eye': Tile.from_masks([33]),
                    'joker_count': 0,
                },
                {
                    'triplets': [Tile.from_masks([38, 38, 38])],
                    'sequences':[Tile.from_masks([33, 34, 35])],
                    'eye': Tile.from_masks([36]),
                    'joker_count': 0,
                },
                {
                    'triplets': [],
                    'sequences':[Tile.from_masks([33, 34, 35]),
                                 Tile.from_masks([36, 38])],
                    'eye': Tile.from_masks([38, 38]),
                    'joker_count': 0,
                }
            ]
        )

        tiles = Tile.from_masks([33, 34, 35, 38, 38, 38])
        self.assertListEqual(list(combinations(tiles, 1)), [])

        tiles = Tile.from_masks([33, 34, 35, 38, 38, 38])
        self.assertListEqual(
            list(combinations(tiles, 2)),
            [
                {
                    'triplets': [Tile.from_masks([38, 38, 38])],
                    'sequences':[Tile.from_masks([34, 35])],
                    'eye': Tile.from_masks([33]),
                    'joker_count': 0,
                },
                {
                    'triplets': [Tile.from_masks([38, 38, 38])],
                    'sequences':[Tile.from_masks([33, 35])],
                    'eye': Tile.from_masks([34]),
                    'joker_count': 0,
                },
                {
                    'triplets': [Tile.from_masks([38, 38, 38])],
                    'sequences':[Tile.from_masks([33, 34])],
                    'eye': Tile.from_masks([35]),
                    'joker_count': 0,
                },
                {
                    'triplets': [Tile.from_masks([38, 38])],
                    'sequences':[Tile.from_masks([33, 34, 35])],
                    'eye': Tile.from_masks([38]),
                    'joker_count': 0,
                },
                {
                    'triplets': [Tile.from_masks([38])],
                    'sequences':[Tile.from_masks([33, 34, 35])],
                    'eye': Tile.from_masks([38, 38]),
                    'joker_count': 0,
                },
                {
                    'triplets': [],
                    'sequences':[Tile.from_masks([33, 34, 35]),
                                 Tile.from_masks([38])],
                    'eye': Tile.from_masks([38, 38]),
                    'joker_count': 0,
                },
                {
                    'triplets': [Tile.from_masks([38, 38, 38])],
                    'sequences':[Tile.from_masks([33, 34, 35])],
                    'eye': [],
                    'joker_count': 0,
                },
            ]
        )

        tiles = Tile.from_masks([33, 33, 33, 38, 38, 38])
        self.assertListEqual(
            list(combinations(tiles, 2)),
            [
                {
                    'triplets': [Tile.from_masks([33, 33]),
                                 Tile.from_masks([38, 38, 38])],
                    'sequences':[],
                    'eye': Tile.from_masks([33]),
                    'joker_count': 0,
                },
                {
                    'triplets': [Tile.from_masks([33]),
                                 Tile.from_masks([38, 38, 38])],
                    'sequences':[],
                    'eye': Tile.from_masks([33, 33]),
                    'joker_count': 0,
                },
                {
                    'triplets': [Tile.from_masks([38, 38, 38])],
                    'sequences':[Tile.from_masks([33])],
                    'eye': Tile.from_masks([33, 33]),
                    'joker_count': 0,
                },
                {
                    'triplets': [Tile.from_masks([33, 33, 33]),
                                 Tile.from_masks([38, 38])],
                    'sequences':[],
                    'eye': Tile.from_masks([38]),
                    'joker_count': 0,
                },
                {
                    'triplets': [Tile.from_masks([33, 33, 33]),
                                 Tile.from_masks([38])],
                    'sequences':[],
                    'eye': Tile.from_masks([38, 38]),
                    'joker_count': 0,
                },
                {
                    'triplets': [Tile.from_masks([33, 33, 33])],
                    'sequences':[Tile.from_masks([38])],
                    'eye': Tile.from_masks([38, 38]),
                    'joker_count': 0,
                },
                {
                    'triplets': [Tile.from_masks([33, 33, 33]),
                                 Tile.from_masks([38, 38, 38])],
                    'sequences':[],
                    'eye': [],
                    'joker_count': 0,
                },
            ]
        )

        self.assertListEqual(
            list(combinations([], 2)),
            [{'triplets': [], 'sequences': [], 'eye': [], 'joker_count': 0}]
        )

        tiles = Tile.from_masks([33, 33, 34, 34, 35, 35, 36, 36, 37, 37])
        self.assertEqual(len(list(combinations(tiles, 4))), 359)
