from collections import defaultdict

__all__ = [
    'is_same_rank', 'is_same_suit', 'is_rank_consecutive', 'is_rank_one_gap'
]

transformation = {1: 'single', 2: 'pair', 3: 'triplet', 4: 'multiple'}


def is_same_rank(cards):
    if not cards:
        return False
    if len(cards) == 1:
        return True
    base = cards[0].rank
    return all(card.rank == base for card in cards)


def is_same_suit(cards):
    if not cards:
        return False
    if len(cards) == 1:
        return True
    base = cards[0].suit
    return all(base == card.suit for card in cards)


def is_rank_one_gap(cards):
    has_gap, gap_position = False, None
    for index in range(len(cards) - 1):
        ascend_by = cards[index + 1].rank - cards[index].rank
        if has_gap:
            if ascend_by != 1:
                has_gap, gap_position = False, None
                break
        else:
            if ascend_by == 2:
                has_gap = True
                gap_position = index + 1
            elif ascend_by != 1:
                has_gap, gap_position = False, None
                break
    assert not has_gap or gap_position is not None
    return has_gap, gap_position


def is_rank_consecutive(cards):
    '''Check the hand cards with consecutive, the suit is ignored'''
    card_count = len(cards)
    if card_count == 0:
        return False
    if card_count == 1:
        return True

    for index in range(card_count - 1):
        if cards[index + 1].rank - cards[index].rank != 1:
            return False
    return True


def get_properties(cards):
    counter = defaultdict(list)
    for card in cards:
        counter[card.rank].append(card)
    properties = {
        'cards': cards,
        'same_suit': is_same_suit(cards),
        'consecutive': is_rank_consecutive(cards),
        'single': [],
        'pair': [],
        'triplet': [],
        'multiple': [],
    }
    for cards in counter.values():
        properties[transformation.get(len(cards), 'multiple')].append(cards)
    return properties
