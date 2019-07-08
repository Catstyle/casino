from unittest import TestCase

from casino.exceptions import InvalidInstance
from casino.poker import Card

d3 = Card.DIAMOND_THREE
d4 = Card.DIAMOND_FOUR
d5 = Card.DIAMOND_FIVE
d6 = Card.DIAMOND_SIX
d2 = Card.DIAMOND_TWO

h4 = Card.HEART_FOUR


class CardTest(TestCase):

    def test_suits(self):
        self.assertTupleEqual(Card.NORMAL_SUITS, (1, 2, 3, 4))
        self.assertTupleEqual(Card.SUITS, (1, 2, 3, 4, 5, 6))

    def test_ranks(self):
        self.assertTupleEqual(
            Card.NORMAL_RANKS, (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16)
        )
        self.assertTupleEqual(Card.JOKER_RANKS, (20, 21))

    def test_special(self):
        Card(Card.SUIT_SPECIAL, Card.RANK_TWO)

    def test_invalid(self):
        with self.assertRaises(InvalidInstance):
            Card.from_mask(1)
        with self.assertRaises(InvalidInstance):
            Card(10, 10)

    def test_mask(self):
        card = Card(Card.SUIT_DIAMOND, Card.RANK_TWO)
        self.assertEqual(card.mask, d2.mask)
        self.assertEqual(Card.from_mask(d2.mask), card)

    def test_masks(self):
        card = Card(Card.SUIT_DIAMOND, Card.RANK_TWO)
        card2 = Card(Card.SUIT_DIAMOND, Card.RANK_THREE)
        self.assertListEqual(
            Card.from_masks([d2.mask, d3.mask]), [card, card2]
        )

    def test_str(self):
        card = Card(Card.SUIT_DIAMOND, Card.RANK_TWO)
        self.assertEqual(str(card), '[DIAMOND,TWO]')

    def test_sort_order(self):
        cards = Card.from_masks([d3.mask, d4.mask])
        cards.sort()
        self.assertListEqual([card.mask for card in cards], [d3.mask, d4.mask])

        cards = Card.from_masks([d4.mask, d3.mask])
        cards.sort()
        self.assertListEqual([card.mask for card in cards], [d3.mask, d4.mask])

    def test_add(self):
        card = Card(Card.SUIT_DIAMOND, Card.RANK_THREE)
        self.assertEqual(card + 1, Card(Card.SUIT_DIAMOND, Card.RANK_FOUR))

    def test_sub(self):
        card = Card(Card.SUIT_DIAMOND, Card.RANK_FOUR)
        self.assertEqual(card - 1, Card(Card.SUIT_DIAMOND, Card.RANK_THREE))

    def test_invalid_add(self):
        card = Card(Card.SUIT_DIAMOND, Card.RANK_TWO)
        with self.assertRaises(InvalidInstance):
            card + 20
        with self.assertRaises(TypeError):
            card + '1'

    def test_eq(self):
        self.assertEqual(
            Card.from_mask(Card.DIAMOND_THREE.mask),
            Card.from_mask(Card.DIAMOND_THREE.mask)
        )
        self.assertEqual(
            Card.from_mask(Card.DIAMOND_THREE.mask),
            Card(Card.SUIT_DIAMOND, Card.RANK_THREE)
        )

    def test_ne(self):
        self.assertNotEqual(d3, d4)

    def test_lt(self):
        self.assertLessEqual(d3, d4)
        self.assertLessEqual(d3, h4)
        self.assertLessEqual(h4, d5)

    def test_gt(self):
        self.assertGreaterEqual(d4, d3)
        self.assertGreaterEqual(h4, d4)
        self.assertGreaterEqual(d5, h4)

    def test_hashable(self):
        tile_set = set([d3, d3])
        self.assertEqual(len(tile_set), 1)
        self.assertIn(d3, tile_set)
        self.assertNotIn(d4, tile_set)

        tile_set = set([d3, h4])
        self.assertEqual(len(tile_set), 2)
