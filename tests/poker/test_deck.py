from unittest import TestCase

from casino.poker import Card, Deck
from casino.utils import random_shuffle_algorithm

d3 = Card.DIAMOND_THREE
da = Card.DIAMOND_ACE

c3 = Card.CLUB_THREE
h3 = Card.HEART_THREE
s3 = Card.SPADE_THREE


class TileTest(TestCase):

    def setUp(self):
        self.deck = Deck(Card.create_cards(with_joker=True))

    def test_deck(self):
        deck = self.deck
        tile = d3
        self.assertEqual(len(deck), 54)
        self.assertEqual(deck[0], tile)
        self.assertIn(tile, deck)

    def test_deck_shuffle(self):
        deck = self.deck
        cards = deck.cards[:]
        self.assertEqual(cards, deck.cards)
        random_shuffle_algorithm(deck.cards)
        self.assertNotEqual(cards, deck.cards)

    def test_deck_sort(self):
        deck = self.deck
        cards = deck.cards[:]
        self.assertListEqual(cards, deck.cards)
        random_shuffle_algorithm(deck.cards)
        self.assertNotEqual(cards, deck.cards)

        deck.sort()
        self.assertEqual(cards, deck.cards)

    def test_deck_exclude_suit(self):
        deck = self.deck
        deck.exclude_suit([Card.SUIT_DIAMOND])
        self.assertEqual(len(deck), 41)
        self.assertNotIn(d3, deck)

    def test_deck_exclude_rank(self):
        deck = self.deck
        deck.exclude_rank([Card.RANK_ACE])
        self.assertEqual(len(deck), 50)
        self.assertNotIn(da, deck)

    def test_slice(self):
        deck = self.deck
        cards = [d3, c3, h3, s3]
        self.assertListEqual(deck[:4], cards)
