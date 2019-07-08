from unittest import TestCase

from casino.exceptions import InvalidInstance
from casino.wordplate import Card

l2 = Card.LOWER_TWO
l3 = Card.LOWER_THREE
l4 = Card.LOWER_FOUR


class CardTest(TestCase):

    def test_suits(self):
        self.assertTupleEqual(Card.SUITS, (1, 2))

    def test_ranks(self):
        self.assertTupleEqual(Card.RANKS, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))

    def test_invalid(self):
        with self.assertRaises(InvalidInstance):
            Card.from_mask(1)
        with self.assertRaises(InvalidInstance):
            Card(10, 10)

    def test_mask(self):
        card = Card(Card.SUIT_LOWER, Card.RANK_TWO)
        self.assertEqual(card.mask, l2.mask)
        self.assertEqual(Card.from_mask(l2.mask), card)

    def test_masks(self):
        card = Card(Card.SUIT_LOWER, Card.RANK_TWO)
        card2 = Card(Card.SUIT_LOWER, Card.RANK_THREE)
        self.assertListEqual(
            Card.from_masks([l2.mask, l3.mask]), [card, card2]
        )

    def test_str(self):
        card = Card(Card.SUIT_LOWER, Card.RANK_TWO)
        self.assertEqual(str(card), '[LOWER,TWO]')

    def test_sort_order(self):
        cards = Card.from_masks([l3.mask, l4.mask])
        cards.sort()
        self.assertListEqual([card.mask for card in cards], [l3.mask, l4.mask])

        cards = Card.from_masks([l4.mask, l3.mask])
        cards.sort()
        self.assertListEqual([card.mask for card in cards], [l3.mask, l4.mask])

    def test_add(self):
        card = Card(Card.SUIT_LOWER, Card.RANK_THREE)
        self.assertEqual(card + 1, Card(Card.SUIT_LOWER, Card.RANK_FOUR))

    def test_sub(self):
        card = Card(Card.SUIT_LOWER, Card.RANK_FOUR)
        self.assertEqual(card - 1, Card(Card.SUIT_LOWER, Card.RANK_THREE))

    def test_invalid_add(self):
        card = Card(Card.SUIT_LOWER, Card.RANK_TWO)
        with self.assertRaises(InvalidInstance):
            card + 20
        with self.assertRaises(TypeError):
            card + '1'

    def test_eq(self):
        self.assertEqual(
            Card.from_mask(Card.LOWER_THREE.mask),
            Card.from_mask(Card.LOWER_THREE.mask)
        )
        self.assertEqual(
            Card.from_mask(Card.LOWER_THREE.mask),
            Card(Card.SUIT_LOWER, Card.RANK_THREE)
        )

    def test_ne(self):
        self.assertNotEqual(l3, l4)

    def test_hashable(self):
        tile_set = set([l3, l3])
        self.assertEqual(len(tile_set), 1)
        self.assertIn(l3, tile_set)
        self.assertNotIn(l4, tile_set)

        tile_set = set([l3, l4])
        self.assertEqual(len(tile_set), 2)
