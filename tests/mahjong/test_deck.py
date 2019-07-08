from unittest import TestCase

from casino.mahjong import Tile, Deck
from casino.utils import random_shuffle_algorithm


class TileTest(TestCase):

    def setUp(self):
        self.deck = Deck(Tile.create_tiles(with_wind=False, with_dragon=False))

    def test_deck(self):
        deck = self.deck
        tile = Tile.from_mask(33)
        self.assertEqual(len(deck), 108)
        self.assertEqual(deck[0], tile)
        self.assertListEqual(deck[:4], [tile] * 4)
        self.assertIn(tile, deck)
        self.assertEqual(
            str(deck),
            '[CHARACTER,ONE]|[CHARACTER,ONE]|[CHARACTER,ONE]|[CHARACTER,ONE]|'
            '[CHARACTER,TWO]|[CHARACTER,TWO]|[CHARACTER,TWO]|[CHARACTER,TWO]|'
            '[CHARACTER,THREE]|[CHARACTER,THREE]|[CHARACTER,THREE]|'
            '[CHARACTER,THREE]|[CHARACTER,FOUR]|[CHARACTER,FOUR]|'
            '[CHARACTER,FOUR]|[CHARACTER,FOUR]|[CHARACTER,FIVE]|'
            '[CHARACTER,FIVE]|[CHARACTER,FIVE]|[CHARACTER,FIVE]'
            '|[CHARACTER,SIX]|[CHARACTER,SIX]|[CHARACTER,SIX]|'
            '[CHARACTER,SIX]|[CHARACTER,SEVEN]|[CHARACTER,SEVEN]|'
            '[CHARACTER,SEVEN]|[CHARACTER,SEVEN]|[CHARACTER,EIGHT]|'
            '[CHARACTER,EIGHT]|[CHARACTER,EIGHT]|[CHARACTER,EIGHT]|'
            '[CHARACTER,NINE]|[CHARACTER,NINE]|[CHARACTER,NINE]|'
            '[CHARACTER,NINE]|[DOT,ONE]|[DOT,ONE]|[DOT,ONE]|[DOT,ONE]|'
            '[DOT,TWO]|[DOT,TWO]|[DOT,TWO]|[DOT,TWO]|[DOT,THREE]|[DOT,THREE]|'
            '[DOT,THREE]|[DOT,THREE]|[DOT,FOUR]|[DOT,FOUR]|[DOT,FOUR]|'
            '[DOT,FOUR]|[DOT,FIVE]|[DOT,FIVE]|[DOT,FIVE]|[DOT,FIVE]|'
            '[DOT,SIX]|[DOT,SIX]|[DOT,SIX]|[DOT,SIX]|[DOT,SEVEN]|[DOT,SEVEN]|'
            '[DOT,SEVEN]|[DOT,SEVEN]|[DOT,EIGHT]|[DOT,EIGHT]|[DOT,EIGHT]|'
            '[DOT,EIGHT]|[DOT,NINE]|[DOT,NINE]|[DOT,NINE]|[DOT,NINE]|'
            '[BAMBOO,ONE]|[BAMBOO,ONE]|[BAMBOO,ONE]|[BAMBOO,ONE]|[BAMBOO,TWO]|'
            '[BAMBOO,TWO]|[BAMBOO,TWO]|[BAMBOO,TWO]|[BAMBOO,THREE]|'
            '[BAMBOO,THREE]|[BAMBOO,THREE]|[BAMBOO,THREE]|[BAMBOO,FOUR]|'
            '[BAMBOO,FOUR]|[BAMBOO,FOUR]|[BAMBOO,FOUR]|[BAMBOO,FIVE]|'
            '[BAMBOO,FIVE]|[BAMBOO,FIVE]|[BAMBOO,FIVE]|[BAMBOO,SIX]|'
            '[BAMBOO,SIX]|[BAMBOO,SIX]|[BAMBOO,SIX]|[BAMBOO,SEVEN]|'
            '[BAMBOO,SEVEN]|[BAMBOO,SEVEN]|[BAMBOO,SEVEN]|[BAMBOO,EIGHT]|'
            '[BAMBOO,EIGHT]|[BAMBOO,EIGHT]|[BAMBOO,EIGHT]|[BAMBOO,NINE]|'
            '[BAMBOO,NINE]|[BAMBOO,NINE]|[BAMBOO,NINE]'
        )

    def test_deck_full(self):
        deck = Deck(Tile.create_tiles())
        self.assertEqual(len(deck), 136)
        self.assertEqual(deck[-1], Tile.from_mask(176))  # WHITE

    def test_deck_shuffle(self):
        deck = self.deck
        tiles = deck.tiles[:]
        self.assertEqual(tiles, deck.tiles)
        random_shuffle_algorithm(deck.tiles)
        self.assertNotEqual(tiles, deck.tiles)

    def test_deck_sort(self):
        deck = self.deck
        tiles = deck.tiles[:]
        self.assertEqual(tiles, deck.tiles)
        random_shuffle_algorithm(deck.tiles)
        self.assertNotEqual(tiles, deck.tiles)

        deck.sort()
        self.assertEqual(tiles, deck.tiles)

    def test_deck_exclude_suit(self):
        deck = self.deck
        deck.exclude_suit([Tile.SUIT_BAMBOO])
        self.assertEqual(len(deck), 72)
        self.assertNotIn(Tile.from_mask(98), deck)

    def test_deck_exclude_rank(self):
        deck = self.deck
        deck.exclude_rank([Tile.RANK_ONE])
        self.assertEqual(len(deck), 96)
        self.assertNotIn(Tile.from_mask(33), deck)
