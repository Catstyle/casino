from collections import defaultdict


class SuitRankBase(type):

    def __init__(cls, name, bases, attrs):
        super(SuitRankBase, cls).__init__(name, bases, attrs)
        for base in bases:
            for name, attr in base.__dict__.items():
                if ((name.startswith('SUIT_') or name.startswith('RANK_')) and
                        isinstance(attr, int)):
                    attrs.setdefault(name, attr)
        cls.SUITS = []
        cls.RANKS = []
        cls.SUIT_NAMES = {}
        cls.RANK_NAMES = {}

        cls._cached = defaultdict(dict)
        cls._initialize_suit(attrs)
        cls._initialize_rank(attrs)
        cls._initialize_properties()
        cls._initialize_instances()

    def _initialize_suit(cls, attrs):
        for name, attr in attrs.items():
            if name.startswith('SUIT_'):
                cls.SUITS.append(attr)
                cls.SUIT_NAMES[attr] = name[5:]
        cls.SUITS.sort()
        cls.SUITS = tuple(cls.SUITS)

    def _initialize_rank(cls, attrs):
        for name, attr in attrs.items():
            if name.startswith('RANK_'):
                cls.RANKS.append(attr)
                cls.RANK_NAMES[attr] = name[5:]
        cls.RANKS.sort()
        cls.RANKS = tuple(cls.RANKS)

    def __call__(cls, suit, rank):
        if rank not in cls._cached[suit]:
            card = super(SuitRankBase, cls).__call__(suit, rank)
            cls._cached[suit][rank] = card
            setattr(cls, card.suit_name + '_' + card.rank_name, card)
        return cls._cached[suit][rank]


class PatternMeta(type):

    def __new__(cls, name, bases, attrs):
        if 'POINT' not in attrs:
            attrs['POINT'] = sum(getattr(base, 'POINT', 0) for base in bases)
        return type.__new__(cls, name, bases, attrs)

    def __str__(cls):
        return '{}'.format(cls.__name__)
    __repr__ = __str__

    def __unicode__(cls):
        return u'{}'.format(cls.__name__)
