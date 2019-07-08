import random
from unittest import TestCase

from casino.wordplate.card import Card
from casino.wordplate.hand import HandCard
from casino.wordplate.manager import Manager
from casino.wordplate.patterns import Normal
from casino.wordplate.properties import filter_sequence_1_5_10

l1 = Card.LOWER_ONE
l2 = Card.LOWER_TWO
l3 = Card.LOWER_THREE
l4 = Card.LOWER_FOUR
l5 = Card.LOWER_FIVE
l7 = Card.LOWER_SEVEN
l10 = Card.LOWER_TEN

u3 = Card.UPPER_THREE


class MahjongTest(TestCase):

    def setUp(self):
        self.manager = Manager()
        self.manager.reset(Card.NORMAL_CARDS, random)

    def test_register_patterns(self):
        manager = self.manager
        self.assertListEqual(manager.patterns, [])
        manager.register_patterns([Normal])
        self.assertListEqual(manager.patterns, [Normal])

    def test_get_pattern(self):
        manager = self.manager
        manager.register_patterns([Normal])

        cards = [l3, l3]
        self.assertIsNotNone(manager.get_pattern(HandCard(cards)))

        cards = [l3, l3, l3]
        self.assertIsNotNone(manager.get_pattern(HandCard(cards)))

        cards = [l3, l3, l4, l4, l5, l5]
        self.assertIsNotNone(manager.get_pattern(HandCard(cards)))

        self.assertIsNone(manager.get_pattern(HandCard([])))

    def test_get_pattern_with_card(self):
        manager = self.manager
        manager.register_patterns([Normal])

        get_pattern_with_card = manager.get_pattern_with_card
        for cards, card in (([l3], l3),
                            ([l3, l3], l3),
                            ([l3, l4, l4, l5, l5], l3),
                            ([l3, l3, l4, l4, l5], l5)):
            self.assertIsNotNone(get_pattern_with_card(HandCard(cards), card))

        self.assertIsNotNone(
            get_pattern_with_card(HandCard([l3, l3]), l3, False)
        )

        self.assertIsNone(get_pattern_with_card(HandCard([]), l3))

    def test_check_win(self):
        cards = [l3, l3]
        self.assertTrue(self.manager.check_win(HandCard(cards)))

        cards = [l3, l3, l4, l4, l5, l5]
        self.assertTrue(self.manager.check_win(HandCard(cards)))

        cards = [Card.LOWER_TWO, Card.LOWER_SEVEN, Card.LOWER_TEN]
        self.assertTrue(self.manager.check_win(HandCard(cards)))

        cards = [l3, u3]
        self.assertFalse(self.manager.check_win(HandCard(cards)))

        cards = [l3]
        self.assertFalse(self.manager.check_win(HandCard(cards)))

    def test_check_win_with_card(self):
        cards = [l3]
        self.assertTrue(self.manager.check_win_with_card(HandCard(cards), l3))

        cards = [l3, l3]
        self.assertTrue(self.manager.check_win_with_card(HandCard(cards), l3))

        cards = [l3, l3]
        self.assertTrue(
            self.manager.check_win_with_card(HandCard(cards), l3, False)
        )

        cards = [l3, l3, l4, l4, l5]
        self.assertTrue(self.manager.check_win_with_card(HandCard(cards), l5))

        cards = [Card.LOWER_TWO, Card.LOWER_SEVEN]
        self.assertTrue(
            self.manager.check_win_with_card(HandCard(cards), Card.LOWER_TEN)
        )

        cards = [l3]
        self.assertFalse(self.manager.check_win_with_card(HandCard(cards), u3))

    def test_has_candidate(self):
        manager = self.manager
        manager.chow_filter.append(filter_sequence_1_5_10)

        for cards in ([l3], [l3, l3], [l3, u3], [l3, l4], [l2, l7], [l1, l5]):
            self.assertTrue(manager.has_candidates(cards), cards)

        for cards in ([], [l2, l5], [l1, l7]):
            self.assertFalse(manager.has_candidates(cards), cards)

    def test_check_chow(self):
        check_chow = self.manager.check_chow

        cards = [l3, l3]
        self.assertListEqual(check_chow(HandCard(cards), u3), [[l3, l3, u3]])

        cards = [l3, l3, l4, l4, l5]
        self.assertListEqual(
            check_chow(HandCard(cards), l5),
            [[l3, l4, l5, l3, l4, l5]],
        )

        cards = [l2, l7]
        self.assertListEqual(check_chow(HandCard(cards), l10), [[l2, l7, l10]])

        cards = [l1, l5]
        self.assertListEqual(check_chow(HandCard(cards), l10), [])

        self.manager.chow_filter.append(filter_sequence_1_5_10)
        self.assertListEqual(check_chow(HandCard(cards), l10), [[l1, l5, l10]])

        cards = [l3]
        self.assertListEqual(check_chow(HandCard(cards), u3), [])

    def test_check_chow_cards(self):
        check_chow_cards = self.manager.check_chow_cards

        cards = [l3, l4, l5]
        self.assertTrue(check_chow_cards(cards))

        cards = [l3, l3, l4, l4, l5, l5]
        self.assertFalse(check_chow_cards(cards))

        cards = [l3, l4, l5, l3, l4, l5]
        self.assertTrue(check_chow_cards(cards))

        cards = [l2, l7, l10]
        self.assertTrue(check_chow_cards(cards))

        cards = [l1, l5, l10]
        self.assertFalse(check_chow_cards(cards))

        self.manager.chow_filter.append(filter_sequence_1_5_10)
        self.assertTrue(check_chow_cards(cards))

        cards = [l3, l4]
        self.assertFalse(check_chow_cards(cards))

        cards = [l3, l4]
        self.assertFalse(check_chow_cards(cards))

    def test_chow(self):
        chow = self.manager.chow
        self.manager.chow_filter.append(filter_sequence_1_5_10)

        for cards in ([l3, l4, l5],
                      [l3, l4, l5, l3, l4, l5],
                      [l2, l7, l10],
                      [l1, l5, l10]):
            handcard = HandCard(cards)
            self.assertListEqual(handcard.used_cards['chow'], [])
            chow(handcard, cards)
            self.assertListEqual(handcard.used_cards['chow'], [cards])

    def test_check_pong(self):
        check_pong = self.manager.check_pong

        cards = [l3, l3]
        self.assertTrue(check_pong(HandCard(cards), l3))

        # triplet cannot separately use
        cards = [l3, l3, l3, l4, l5]
        self.assertFalse(check_pong(HandCard(cards), l3))

        cards = [l3, l4]
        self.assertFalse(check_pong(HandCard(cards), l3))

        cards = [l3, u3]
        self.assertFalse(check_pong(HandCard(cards), l3))

    def test_pong(self):
        handcard = HandCard([l3, l3])
        self.assertListEqual(handcard.used_cards['pong'], [])
        self.manager.pong(handcard, l3)
        self.assertListEqual(handcard.used_cards['pong'], [[l3, l3, l3]])

        # wei
        handcard = HandCard([l3, l3])
        self.assertListEqual(handcard.used_cards['pong'], [])
        self.manager.concealed_pong(handcard, l3)
        self.assertListEqual(
            handcard.used_cards['concealed_pong'], [[l3, l3, l3]]
        )

    def test_check_exposed_kong(self):
        manager = self.manager
        check_kong = manager.check_exposed_kong

        cards = [l3, l3, l3]
        self.assertTrue(check_kong(HandCard(cards), l3))

        cards = [l3, l3]
        handcard = HandCard(cards)
        manager.concealed_pong(handcard, l3)
        self.assertTrue(check_kong(handcard, l3))

        cards = [l3, l3]
        handcard = HandCard(cards)
        manager.pong(handcard, l3)
        self.assertTrue(check_kong(handcard, l3, with_pong=True))

        cards = [l3, l3, u3]
        self.assertFalse(check_kong(HandCard(cards), l3))

    def test_exposed_kong(self):
        handcard = HandCard([l3, l3, l3])
        self.assertListEqual(handcard.used_cards['exposed_kong'], [])
        self.manager.exposed_kong(handcard, l3)
        self.assertListEqual(
            handcard.used_cards['exposed_kong'], [[l3, l3, l3, l3]]
        )

        # wei
        handcard = HandCard([l3, l3])
        self.assertListEqual(handcard.used_cards['exposed_kong'], [])
        self.manager.concealed_pong(handcard, l3)
        self.manager.exposed_kong(handcard, l3)
        self.assertListEqual(
            handcard.used_cards['exposed_kong'], [[l3, l3, l3, l3]]
        )

        # wei
        handcard = HandCard([l3, l3])
        self.assertListEqual(handcard.used_cards['exposed_kong'], [])
        self.manager.pong(handcard, l3)
        self.manager.exposed_kong(handcard, l3)
        self.assertListEqual(
            handcard.used_cards['exposed_kong'], [[l3, l3, l3, l3]]
        )

    def test_check_concealed_kong(self):
        manager = self.manager
        check_kong = manager.check_concealed_kong

        cards = [l3, l3, l3]
        self.assertTrue(check_kong(HandCard(cards), l3))

        cards = [l3, l3]
        handcard = HandCard(cards)
        manager.concealed_pong(handcard, l3)
        self.assertTrue(check_kong(handcard, l3))

        cards = [l3, l3, u3]
        self.assertFalse(check_kong(HandCard(cards), l3))

    def test_concealed_kong(self):
        handcard = HandCard([l3, l3, l3])
        self.assertListEqual(handcard.used_cards['concealed_kong'], [])
        self.manager.concealed_kong(handcard, l3)
        self.assertListEqual(
            handcard.used_cards['concealed_kong'], [[l3, l3, l3, l3]]
        )

        # wei
        handcard = HandCard([l3, l3])
        self.assertListEqual(handcard.used_cards['concealed_kong'], [])
        self.manager.concealed_pong(handcard, l3)
        self.manager.concealed_kong(handcard, l3)
        self.assertListEqual(
            handcard.used_cards['concealed_kong'], [[l3, l3, l3, l3]]
        )

    def test_combinations(self):
        get_combinations = self.manager.get_combinations

        cards = [l3, l3]
        self.assertListEqual(
            get_combinations(cards),
            [{'eye': [l3, l3], 'triplets': [], 'sequences': []}],
        )

        cards = [l3, l3, l3]
        self.assertListEqual(
            get_combinations(cards),
            [{'eye': [], 'triplets': [[l3, l3, l3]], 'sequences': []}],
        )

        cards = [l3, l3, l3, l2, l7, l10]
        self.assertListEqual(
            get_combinations(cards),
            [{'eye': [], 'triplets': [[l3, l3, l3]],
              'sequences': [[l2, l7, l10]]}],
        )

        cards = [l3, l3, l3, l2, l7, l10, l1, l5, l10]
        self.assertListEqual(get_combinations(cards), [])

        self.manager.chow_filter.append(filter_sequence_1_5_10)
        self.assertListEqual(
            get_combinations(cards),
            [{'eye': [], 'triplets': [[l3, l3, l3]],
              'sequences': [[l2, l7, l10], [l1, l5, l10]]}],
        )
