from unittest import TestCase

from casino.wordplate.card import Card
from casino.wordplate.hand import HandCard
from casino.wordplate.manager import Manager
from casino.wordplate.patterns import Normal
from casino.wordplate.properties import filter_sequence_1_5_10

l1 = Card.LOWER_ONE
l3 = Card.LOWER_THREE
l4 = Card.LOWER_FOUR
l5 = Card.LOWER_FIVE
l10 = Card.LOWER_TEN


class PatternTest(TestCase):

    def test_normal(self):
        manager = Manager()
        manager.register_patterns([Normal])
        get_pattern = manager.get_pattern

        for cards in ([l3, l3], [l3, l3, l3]):
            self.assertIs(get_pattern(HandCard(cards)), Normal)

        for cards in ([l3, l4], [l3], [l1, l5, l10]):
            self.assertIsNot(get_pattern(HandCard(cards)), Normal)

        manager.chow_filter.append(filter_sequence_1_5_10)
        cards = [l1, l5, l10]
        self.assertIs(get_pattern(HandCard(cards)), Normal)
