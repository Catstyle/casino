from unittest import TestCase

from casino.poker import Card
from casino.poker.properties import (
    is_same_suit, is_same_rank, is_rank_one_gap, is_rank_consecutive,
    get_properties,
)

d3 = Card.DIAMOND_THREE
d4 = Card.DIAMOND_FOUR
d5 = Card.DIAMOND_FIVE
d6 = Card.DIAMOND_SIX
dj = Card.DIAMOND_JACK
dq = Card.DIAMOND_QUEEN

c3 = Card.CLUB_THREE
c4 = Card.CLUB_FOUR
c5 = Card.CLUB_FIVE


class PropertiesTest(TestCase):

    def test_is_same_suit(self):
        self.assertTrue(is_same_suit([d3, d4, d5, d6]))
        self.assertFalse(is_same_suit([d3, d4, d5, d6, c3]))
        self.assertFalse(is_same_suit([]))
        self.assertTrue(is_same_suit([d3]))

    def test_is_same_rank(self):
        self.assertTrue(is_same_rank([d3, c3]))
        self.assertFalse(is_same_rank([d3, d4]))
        self.assertFalse(is_same_rank([]))
        self.assertTrue(is_same_rank([d3]))

    def test_is_rank_one_gap(self):
        cards = [d3, d5, d6]
        has_gap, gap_position = is_rank_one_gap(cards)
        self.assertTrue(has_gap)
        self.assertEqual(gap_position, 1)

        cards = [d3, d4, d5]
        has_gap, gap_position = is_rank_one_gap(cards)
        self.assertFalse(has_gap)
        self.assertIsNone(gap_position)

        cards = [d3, dj, dq]
        has_gap, gap_position = is_rank_one_gap(cards)
        self.assertFalse(has_gap)
        self.assertIsNone(gap_position)

        cards = [d3, d5, dq]
        has_gap, gap_position = is_rank_one_gap(cards)
        self.assertFalse(has_gap)
        self.assertIsNone(gap_position)

    def test_is_rank_consecutive(self):
        self.assertTrue(is_rank_consecutive([d3, d4, d5, d6]))
        self.assertFalse(is_rank_consecutive([d3, d4, d5, c3]))
        self.assertFalse(is_rank_consecutive([]))
        self.assertTrue(is_rank_consecutive([d3]))

    def test_get_properties(self):
        cards = [d3, d3, d4, d4, d5, d5]
        self.assertDictEqual(
            get_properties(cards),
            {'cards': cards, 'same_suit': True, 'consecutive': False,
             'single': [], 'pair': [[d3, d3], [d4, d4], [d5, d5]],
             'triplet': [], 'multiple': []}
        )

        cards = [d3, d3, d3, d4, d4, d5, d5]
        self.assertDictEqual(
            get_properties(cards),
            {'cards': cards, 'same_suit': True, 'consecutive': False,
             'single': [], 'pair': [[d4, d4], [d5, d5]],
             'triplet': [[d3, d3, d3]], 'multiple': []}
        )

        cards = [d3, d3, d3, d4, d4, d5, d5, c3]
        self.assertDictEqual(
            get_properties(cards),
            {'cards': cards, 'same_suit': False, 'consecutive': False,
             'single': [], 'pair': [[d4, d4], [d5, d5]],
             'triplet': [], 'multiple': [[d3, d3, d3, c3]]}
        )

        cards = [d3, d3, d3, d4, d4, d5, d5, d6]
        self.assertDictEqual(
            get_properties(cards),
            {'cards': cards, 'same_suit': True, 'consecutive': False,
             'single': [[d6]], 'pair': [[d4, d4], [d5, d5]],
             'triplet': [[d3, d3, d3]], 'multiple': []}
        )

        cards = [d3, d3, d3, c3, c3, d5, d5, d6]
        self.assertDictEqual(
            get_properties(cards),
            {'cards': cards, 'same_suit': False, 'consecutive': False,
             'single': [[d6]], 'pair': [[d5, d5]],
             'triplet': [], 'multiple': [[d3, d3, d3, c3, c3]]}
        )
