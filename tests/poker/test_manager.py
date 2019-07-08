import random
from unittest import TestCase

from casino.poker import Card
from casino.poker.deck import Deck
from casino.poker.manager import PokerManager
from casino.poker.patterns import Pair, Triplet

d3 = Card.DIAMOND_THREE
d4 = Card.DIAMOND_FOUR
d5 = Card.DIAMOND_FIVE


class MahjongTest(TestCase):

    def setUp(self):
        self.deck = Deck(Card.create_cards())
        self.poker_manager = PokerManager()
        self.poker_manager.reset(self.deck, random)

    def test_left_cards(self):
        self.assertEqual(len(self.deck), self.poker_manager.left_cards)

    def test_register_pattern(self):
        manager = self.poker_manager
        self.assertListEqual(manager.patterns, [])
        manager.register_pattern(Pair)
        self.assertListEqual(manager.patterns, [Pair])

    def test_register_patterns(self):
        manager = self.poker_manager
        self.assertListEqual(manager.patterns, [])
        manager.register_patterns([Pair, Triplet])
        self.assertListEqual(manager.patterns, [Triplet, Pair])

    def test_get_pattern(self):
        manager = self.poker_manager
        manager.register_patterns([Pair, Triplet])

        cards = [d3, d3]
        self.assertIsNotNone(manager.get_pattern(cards))

        cards = [d3, d3, d3]
        self.assertIsNotNone(manager.get_pattern(cards))

        cards = [d3, d3, d4, d4, d5, d5]
        self.assertIsNone(manager.get_pattern(cards))

        self.assertIsNone(manager.get_pattern([]))
