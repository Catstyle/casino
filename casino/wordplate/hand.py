from bisect import insort
from collections import Counter
from copy import deepcopy
from itertools import chain


class HandCard(object):

    def __init__(self, cards):
        self.used_cards = {
            'chow': [],
            'pong': [],
            'exposed_kong': [],
            'concealed_pong': [],
            'concealed_kong': [],
        }
        self.set_cards(cards)

    @property
    def masks(self):
        return sorted(
            c.mask for c in chain(self.fixed_cards.elements(), self.cards)
        )

    @property
    def all_cards(self):
        cards = list(chain(self.fixed_cards.elements(), self.cards))
        for value in self.used_cards.values():
            for comb in value:
                cards.extend(comb)
        return cards

    def set_cards(self, cards):
        self.cards = []
        self.fixed_cards = Counter()
        for card, count in Counter(cards).items():
            if count >= 3:
                self.fixed_cards[card] = count
            else:
                self.cards.extend([card] * count)
        self.cards.sort()

    def add_card(self, card):
        insort(self.cards, card)

    def remove_card(self, card):
        self.cards.remove(card)

    def add_cards(self, cards):
        for card in cards:
            insort(self.cards, card)

    def remove_cards(self, cards):
        for card in cards:
            self.cards.remove(card)

    def clone(self):
        ins = self.__class__(self.cards + list(self.fixed_cards.elements()))
        ins.used_cards = deepcopy(self.used_cards)
        return ins

    def __str__(self):
        return '[cards|%s][fixed|%s][used|%s]' % (
            self.cards, self.fixed_cards, self.used_cards
        )
    __unicode__ = __repr__ = __str__
