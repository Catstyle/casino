from bisect import insort

__all__ = ['HandCard']


class HandCard(object):

    def __init__(self, cards):
        self.cards = sorted(cards)

    @property
    def masks(self):
        return [card.mask for card in self.cards]

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

    def __getitem__(self, index):
        return self.cards[index]

    def __getslice__(self, i, j):
        return self.cards[i:j]

    def __len__(self):
        return len(self.cards)

    def __setitem__(self, index, value):
        self.cards[index] = value

    def __str__(self):
        return '[cards|%s]' % self.cards
    __unicode__ = __repr__ = __str__
