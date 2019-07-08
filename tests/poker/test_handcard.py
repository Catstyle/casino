from unittest import TestCase

from casino.poker import Card, HandCard

d3 = Card.DIAMOND_THREE
d4 = Card.DIAMOND_FOUR
d5 = Card.DIAMOND_FIVE
d6 = Card.DIAMOND_SIX
d7 = Card.DIAMOND_SEVEN
d8 = Card.DIAMOND_EIGHT
d9 = Card.DIAMOND_NINE
dj = Card.DIAMOND_JACK
dq = Card.DIAMOND_QUEEN
dk = Card.DIAMOND_KING


class HandCardTest(TestCase):

    def setUp(self):
        self.handcard = HandCard([
            d3, d4, d5, d7, d5, d6, d8, d7, d9, dj, dk
        ])

    def test_handcard(self):
        handcard = self.handcard
        self.assertEqual(len(handcard), 11)
        self.assertListEqual(handcard.masks, [
            d3.mask, d4.mask, d5.mask, d5.mask, d6.mask, d7.mask, d7.mask,
            d8.mask, d9.mask, dj.mask, dk.mask
        ])

    def test_add_card(self):
        handcard = self.handcard
        card = dq
        self.assertNotIn(card, handcard.cards)
        handcard.add_card(card)
        self.assertEqual(len(handcard.cards), 12)
        self.assertIn(card, handcard.cards)

    def test_remove_card(self):
        handcard = self.handcard
        card = dk
        self.assertIn(card, handcard.cards)
        handcard.remove_card(card)
        self.assertEqual(len(handcard.cards), 10)
        self.assertNotIn(card, handcard.cards)

        with self.assertRaises(ValueError):
            handcard.remove_card(card)

        card = d5
        self.assertIn(card, handcard.cards)
        handcard.remove_card(card)
        self.assertEqual(len(handcard.cards), 9)
        self.assertIn(card, handcard.cards)

    def test_add_cards(self):
        handcard = self.handcard
        card = dq
        self.assertNotIn(card, handcard.cards)

        handcard.add_cards([dq, dq, dq])
        self.assertIn(card, handcard.cards)
        self.assertEqual(handcard.cards.count(card), 3)

    def test_remove_cards(self):
        handcard = self.handcard
        card = d5
        self.assertIn(card, handcard.cards)
        self.assertEqual(handcard.cards.count(card), 2)

        handcard.remove_cards([d5, d5])
        self.assertNotIn(card, handcard.cards)
        self.assertEqual(handcard.cards.count(card), 0)

    def test_getitem(self):
        handcard = self.handcard
        card = d3
        self.assertIn(card, handcard.cards)
        self.assertIs(handcard[0], card)

    def test_slice(self):
        handcard = self.handcard
        cards = [d3, d4, d5]
        self.assertListEqual(cards, handcard[:3])

    def test_setitem(self):
        handcard = self.handcard
        card = d3
        self.assertIn(card, handcard.cards)
        self.assertIs(handcard[0], card)

        handcard[0] = d4
        self.assertIsNot(handcard[0], card)
