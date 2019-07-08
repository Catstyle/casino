from functools import total_ordering
from itertools import combinations, chain

from casino.core import PatternMeta
from casino.utils import add_metaclass


@total_ordering
@add_metaclass(PatternMeta)
class BasePattern(object):

    id = None
    POINT = -1

    def __init__(self, properties):
        self.size = 1
        self.properties = properties
        self.max_card = max(properties['cards'])

    @classmethod
    def validate(cls, properties):
        raise NotImplementedError

    @classmethod
    def filter(cls, properties, max_card, size=1, force=False):
        raise NotImplementedError

    def __eq__(self, other):
        return (
            self.POINT == other.POINT and
            self.size == other.size and
            self.max_card.rank == other.max_card.rank
        )

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return (
            self.POINT < other.POINT or
            (self.POINT == other.POINT and
                (self.size < other.size or
                    (self.size == other.size and
                        self.max_card.rank < other.max_card.rank)))
        )

    def __str__(self):
        return '[{},{}]'.format(self.__class__.__name__, self.max_card)
    __repr__ = __unicode__ = __str__


class Single(BasePattern):

    id = 101
    POINT = 0

    @classmethod
    def validate(cls, properties):
        return len(properties['cards']) == 1

    @classmethod
    def filter(cls, properties, max_card, size=1, force=False):
        max_rank = max_card.rank if max_card else 0
        for card in properties['single']:
            if card[0].rank > max_rank:
                return card
        if force:
            max_card = max_card
            for card in properties['cards']:
                if card.rank > max_rank:
                    return (card,)
        return ()


class Pair(BasePattern):

    id = 102
    POINT = 10

    @classmethod
    def validate(cls, properties):
        cards = properties['cards']
        if len(cards) != 2:
            return False
        return cards[0].rank == cards[1].rank

    @classmethod
    def filter(cls, properties, max_card, size=1, force=False):
        cards = properties['pair']
        if force:
            cards = chain(cards, properties['triplet'], properties['multiple'])
        max_rank = max_card.rank if max_card else 0
        for combs in cards:
            if combs[-1].rank > max_rank:
                return combs[:2]
        return ()


class Triplet(BasePattern):

    id = 103
    POINT = 20

    @classmethod
    def validate(cls, properties):
        cards = properties['cards']
        if len(cards) != 3:
            return False
        return cards[0].rank == cards[1].rank == cards[2].rank

    @classmethod
    def filter(cls, properties, max_card, size=1, force=False):
        cards = properties['triplet']
        if force:
            cards = chain(cards, properties['multiple'])
        max_rank = max_card.rank if max_card else 0
        for combs in cards:
            if combs[-1].rank > max_rank:
                return combs[:3]
        return ()


class Pairs(Pair):

    id = 104
    POINT = 30

    def __init__(self, properties):
        super(Pairs, self).__init__(properties)
        self.size = len(properties['pair'])

    @classmethod
    def _validate(cls, ranks):
        base = ranks[0]
        for idx in range(0, len(ranks), 2):
            now = ranks[idx]
            if not ((now - base) * 2 == idx and now == ranks[idx + 1]):
                return False
        return True

    @classmethod
    def validate(cls, properties):
        cards = properties['cards']
        count = len(cards)
        if count < 6 or count % 2 != 0:
            return False
        return cls._validate(sorted(card.rank for card in cards))

    @classmethod
    def filter(cls, properties, max_card, size=3, force=False):
        max_rank = max_card.rank if max_card else 0
        pairs = properties['pair']
        for combs in combinations(sum(pairs, []), size * 2):
            ranks = [card.rank for card in combs]
            if ranks[-1] <= max_rank or not cls._validate(ranks):
                continue
            return combs
        if force:
            cards = chain(pairs, properties['triplet'], properties['multiple'])
            for combs in combinations(sorted(sum(cards, [])), size * 2):
                ranks = [card.rank for card in combs]
                if ranks[-1] <= max_rank or not cls._validate(ranks):
                    continue
                return combs
        return ()


class Triplets(Triplet):

    id = 105
    POINT = 40

    def __init__(self, properties):
        super(Triplets, self).__init__(properties)
        self.size = len(properties['triplet'])

    @classmethod
    def _validate(cls, ranks):
        base = ranks[0]
        for idx in range(0, len(ranks), 3):
            now = ranks[idx]
            if not ((now - base) * 3 == idx and
                    now == ranks[idx + 1] == ranks[idx + 2]):
                return False
        return True

    @classmethod
    def validate(cls, properties):
        cards = properties['cards']
        count = len(cards)
        if count < 6 or count % 3 != 0:
            return False
        return cls._validate(sorted(card.rank for card in cards))

    @classmethod
    def filter(cls, properties, max_card, size=2, force=False):
        max_rank = max_card.rank if max_card else 0
        cards = properties['triplet']
        for combs in combinations(sum(cards, []), size * 3):
            ranks = [card.rank for card in combs]
            if ranks[-1] <= max_rank or not cls._validate(ranks):
                continue
            return combs
        if force:
            cards = chain(cards, properties['multiple'])
            for combs in combinations(sorted(sum(cards, [])), size * 3):
                ranks = [card.rank for card in combs]
                if ranks[-1] <= max_rank or not cls._validate(ranks):
                    continue
                return combs
        return ()
