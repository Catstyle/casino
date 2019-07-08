from operator import attrgetter

from casino.utils import random_shuffle_algorithm

from .card import Card
from .deck import Deck
from .properties import get_properties


class PokerManager(object):

    sort_func = attrgetter('POINT')

    def __init__(self, shuffle_algorithm=None, card_class=Card):
        self.deck = Deck([])
        self.card_class = card_class
        self.shuffle_algorithm = shuffle_algorithm or random_shuffle_algorithm
        self.patterns = []

        self.draw_joker = None
        self.jokers = []
        self.joker_factory = None

    @property
    def left_cards(self):
        return len(self.deck)

    def reset(self, deck, ran):
        self.deck = deck
        self.shuffle_algorithm(deck.cards, ran)

        self.draw_joker = None
        del self.jokers[:]
        if self.joker_factory:
            draw_joker, jokers = self.joker_factory(deck)
            self.draw_joker = draw_joker
            self.jokers = list(jokers)

    def register_pattern(self, pattern, sort_func=None):
        self.patterns.append(pattern)
        self.patterns.sort(key=sort_func or self.sort_func, reverse=True)

    def register_patterns(self, patterns, sort_func=None):
        self.patterns.extend(patterns)
        self.patterns.sort(key=sort_func or self.sort_func, reverse=True)

    def get_pattern(self, cards):
        properties = get_properties(cards)
        for pattern in self.patterns:
            if pattern.validate(properties):
                return pattern(properties)

    def set_joker_factory(self, factory):
        self.joker_factory = factory
