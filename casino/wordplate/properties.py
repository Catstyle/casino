from collections import Counter

from casino.exceptions import InvalidInstance


def filter_sequence(cards, card, joker_count=0):
    for r1, r2 in ((-2, -1), (-1, 1), (1, 2),):
        try:
            comb = sorted([card, card + r1, card + r2])
            if all(c in cards for c in comb):
                yield comb, 0
        except InvalidInstance:
            continue

    if joker_count > 0:
        for delta in (-2, -1, 1, 2):
            try:
                comb = sorted([card, card + delta])
                if all(c in cards for c in comb):
                    yield comb, 1
            except InvalidInstance:
                continue


def filter_triplet(cards, card, joker_count=0):
    if cards.count(card) == 3:
        yield [card, card, card], 0

    if joker_count > 0 and cards.count(card) >= 2:
        yield [card, card], 1


def filter_triplet_rank(cards, card, joker_count=0):
    rank = card.rank
    counter = Counter(c for c in cards if c.rank == rank)

    c = ~card
    if counter[card] >= 2 and counter[c] >= 1:
        yield sorted([card, card, c]), 0

    if counter[card] >= 1 and counter[c] >= 2:
        yield sorted([card, c, c]), 0

    if joker_count > 0:
        if counter[card] >= 2:
            yield sorted([card, card]), 1

        if counter[c] >= 1:
            yield sorted([card, c]), 1


def filter_sequence_2_7_10(cards, card, joker_count=0):
    if card.rank not in {2, 7, 10}:
        return
    suit = card.suit
    cls = card.__class__
    comb = [cls(suit, rank) for rank in (2, 7, 10)]
    if all(c in cards for c in comb):
        yield comb, 0

    if joker_count > 0:
        for rank in {2, 7, 10} - {card.rank}:
            comb = sorted([card, cls(suit, rank)])
            if all(c in cards for c in comb):
                yield comb, 1


def filter_sequence_1_5_10(cards, card, joker_count=0):
    if card.rank not in {1, 5, 10}:
        return
    suit = card.suit
    cls = card.__class__
    comb = [cls(suit, rank) for rank in (1, 5, 10)]
    if all(c in cards for c in comb):
        yield comb, 0

    if joker_count > 0:
        for rank in {1, 5, 10} - {card.rank}:
            comb = sorted([card, cls(suit, rank)])
            if all(c in cards for c in comb):
                yield comb, 1
