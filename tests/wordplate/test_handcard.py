from unittest import TestCase

from casino.wordplate import Card, HandCard

l1 = Card.LOWER_ONE
l2 = Card.LOWER_TWO
l3 = Card.LOWER_THREE
l4 = Card.LOWER_FOUR
l5 = Card.LOWER_FIVE
l6 = Card.LOWER_SIX
l7 = Card.LOWER_SEVEN
l8 = Card.LOWER_EIGHT
l9 = Card.LOWER_NINE
l10 = Card.LOWER_TEN

u8 = Card.UPPER_EIGHT


class HandCardTest(TestCase):

    def setUp(self):
        self.handcard = HandCard([
            l1, l2, l3, l4, l5, l5, l6, l7, l7, l7, l8, l9, l10
        ])

    def test_handcard(self):
        handcard = self.handcard
        self.assertEqual(len(handcard.cards), 10)
        self.assertEqual(len(handcard.fixed_cards), 1)
        self.assertListEqual(handcard.masks, [
            l1.mask, l2.mask, l3.mask, l4.mask, l5.mask, l5.mask, l6.mask,
            l7.mask, l7.mask, l7.mask, l8.mask, l9.mask, l10.mask,
        ])

        self.assertNotIn(l7, handcard.cards)
        self.assertIn(l7, handcard.fixed_cards)
        self.assertEqual(handcard.fixed_cards[l7], 3)

    def test_add_card(self):
        handcard = self.handcard
        card = u8
        self.assertNotIn(card, handcard.cards)
        handcard.add_card(card)
        self.assertEqual(len(handcard.cards), 11)
        self.assertIn(card, handcard.cards)

    def test_remove_card(self):
        handcard = self.handcard
        card = l8
        self.assertIn(card, handcard.cards)
        handcard.remove_card(card)
        self.assertEqual(len(handcard.cards), 9)
        self.assertNotIn(card, handcard.cards)

        with self.assertRaises(ValueError):
            handcard.remove_card(card)

        card = l5
        self.assertIn(card, handcard.cards)
        handcard.remove_card(card)
        self.assertEqual(len(handcard.cards), 8)
        self.assertIn(card, handcard.cards)

    def test_add_cards(self):
        handcard = self.handcard
        card = u8
        self.assertNotIn(card, handcard.cards)

        handcard.add_cards([u8, u8, u8])
        self.assertIn(card, handcard.cards)
        self.assertEqual(handcard.cards.count(card), 3)

    def test_remove_cards(self):
        handcard = self.handcard
        card = l5
        self.assertIn(card, handcard.cards)
        self.assertEqual(handcard.cards.count(card), 2)

        handcard.remove_cards([l5, l5])
        self.assertNotIn(card, handcard.cards)
        self.assertEqual(handcard.cards.count(card), 0)

    def test_set_cards(self):
        handcard = self.handcard
        card = l5
        self.assertIn(card, handcard.cards)
        self.assertEqual(handcard.cards.count(card), 2)
        handcard.add_card(card)
        self.assertEqual(handcard.cards.count(card), 3)

        handcard.set_cards(
            handcard.cards + list(handcard.fixed_cards.elements())
        )
        self.assertEqual(handcard.cards.count(card), 0)
        self.assertIn(card, handcard.fixed_cards)
        self.assertEqual(handcard.fixed_cards[card], 3)
