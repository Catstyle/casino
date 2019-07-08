__all__ = ['Deck']


class Deck(object):

    def __init__(self, cards):
        self.cards = cards
        self.card_set = set(cards)
        self.suits = {card.suit for card in cards}

    def exclude_rank(self, exclude_ranks):
        self.cards = [card for card in self.cards
                      if card.rank not in exclude_ranks]
        return self

    def exclude_suit(self, exclude_suits):
        self.cards = [card for card in self.cards
                      if card.suit not in exclude_suits]
        for suit in exclude_suits:
            self.suits.remove(suit)
        return self

    def select(self, key=None):
        return filter(key or (lambda x: True), self.cards)

    def sort(self):
        self.cards.sort()

    def __getitem__(self, index):
        return self.cards[index]

    def __len__(self):
        return len(self.cards)

    def __getslice__(self, begin, end):
        return self.cards[begin:end]

    def __contains__(self, card):
        return card in self.cards

    def __str__(self):
        return '|'.join([str(card) for card in self.cards])
    __unicode__ = __repr__ = __str__
