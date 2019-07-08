from collections import Counter

__all__ = [
    'is_same_suit', 'is_7_pairs', 'is_7_pairs_with_joker', 'get_lack_of_joker',
    'combinations'
]


def is_same_suit(tiles):
    base = tiles[0].suit
    return all(base == tile.suit for tile in tiles)


def is_rank_consecutive(tiles):
    '''Check the tiles with consecutive, the suit is ignored'''
    count = len(tiles)
    if count == 0:
        return False
    if count == 1:
        return True

    for index in range(count - 1):
        if tiles[index + 1].rank - tiles[index].rank != 1:
            return False
    return True


def is_7_pairs(tiles):
    return len(tiles) == 14 and all(
        tiles[idx] is tiles[idx + 1] for idx in (0, 2, 4, 6, 8, 10, 12)
    )


def is_7_pairs_with_joker(tiles, joker_count):
    count = len(tiles)
    if count + joker_count != 14:
        return False

    idx = 0
    while idx < count and joker_count >= 0:
        if idx + 1 == count:
            joker_count -= 1
            break
        elif tiles[idx] is tiles[idx + 1]:
            idx += 2
        else:
            joker_count -= 1
            idx += 1
    return joker_count % 2 == 0


def sub_combinations(tiles, joker_count=0):
    count = len(tiles)
    if count != 0 and (count + joker_count) % 3 != 0:
        return

    if count < 3:
        if count == 0:
            yield {'triplets': [], 'sequences': [], 'joker_count': joker_count}
        elif count == 1 and joker_count >= 2:
            t1 = tiles[0]
            yield {'triplets': [[t1]], 'sequences': [],
                   'joker_count': joker_count - 2}
            yield {'triplets': [], 'sequences': [[t1]],
                   'joker_count': joker_count - 2}
        elif count == 2 and joker_count >= 1:
            t1, t2 = tiles
            if t1 is t2:
                yield {'triplets': [[t1, t1]], 'sequences': [],
                       'joker_count': joker_count - 1}
            elif (t1.suit in t1.NUMERIC_SUITS and
                    t2.rank < 10 and
                    t2.mask - t1.mask < 3):
                yield {'triplets': [], 'sequences': [[t1, t2]],
                       'joker_count': joker_count - 1}
        return

    t1 = tiles.pop(0)
    if t1 is tiles[0] is tiles[1]:
        for comb in sub_combinations(tiles[2:], joker_count):
            comb['triplets'] = [[t1, t1, t1]] + comb['triplets']
            yield comb

    if t1.rank < 8:
        n1, n2 = t1 + 1, t1 + 2
        ts = tiles[:]
        try:
            ts.remove(n1)
            ts.remove(n2)
        except ValueError:
            pass
        else:
            for comb in sub_combinations(ts, joker_count):
                comb['sequences'] = [[t1, n1, n2]] + comb['sequences']
                yield comb

    if joker_count >= 1:
        free_joker = joker_count - 1
        if t1 is tiles[0]:
            for comb in sub_combinations(tiles[1:], free_joker):
                comb['triplets'] = [[t1, t1]] + comb['triplets']
                yield comb

        if t1.suit in t1.NUMERIC_SUITS:
            for rank in (1, 2):
                if not t1.validate_mask(t1.mask + rank):
                    continue
                t2 = t1 + rank
                ts = tiles[:]
                try:
                    ts.remove(t2)
                except ValueError:
                    continue
                else:
                    for comb in sub_combinations(ts, free_joker):
                        comb['sequences'] = [[t1, t2]] + comb['sequences']
                        yield comb

    if joker_count >= 2:
        for comb in sub_combinations(tiles[:], joker_count - 2):
            comb['triplets'] = [[t1]] + comb['triplets']
            yield comb

        for comb in sub_combinations(tiles[:], joker_count - 2):
            comb['sequences'] = [[t1]] + comb['sequences']
            yield comb


def combinations(tiles, joker_count=0):
    if (len(tiles) + joker_count) % 3 != 2:
        return

    for eye, count in Counter(tiles).items():
        if joker_count >= 1:
            ts = tiles[:]
            ts.remove(eye)
            for comb in sub_combinations(ts, joker_count - 1):
                comb['eye'] = [eye]
                yield comb
        if count >= 2:
            ts = tiles[:]
            ts.remove(eye)
            ts.remove(eye)
            for comb in sub_combinations(ts, joker_count):
                comb['eye'] = [eye, eye]
                yield comb
    if joker_count >= 2:
        for comb in sub_combinations(tiles[:], joker_count - 2):
            comb['eye'] = []
            yield comb


def get_lack_of_joker(suit_tiles, used_count=0, needed_count=4):
    count = len(suit_tiles)
    if count < 3:
        if count == 0:
            return min(used_count, needed_count)
        if count == 1:
            return min(used_count + 2, needed_count)
        t1, t2 = suit_tiles
        if t1.suit not in t1.NUMERIC_SUITS:
            return used_count + 1 if t1 is t2 else needed_count
        else:
            return used_count + 1 if t2.rank - t1.rank < 3 else needed_count

    t1 = suit_tiles.pop(0)
    if t1 is suit_tiles[0] is suit_tiles[1]:
        needed_count = min(
            get_lack_of_joker(suit_tiles[2:], used_count, needed_count),
            needed_count
        )

    if needed_count != 0 and t1.rank < 8:
        ts = suit_tiles[:]
        try:
            ts.remove(t1 + 1)
            ts.remove(t1 + 2)
        except ValueError:
            pass
        else:
            needed_count = min(
                get_lack_of_joker(ts, used_count, needed_count), needed_count
            )

    if used_count + 1 < needed_count:
        ucount = used_count + 1
        if t1 is suit_tiles[0]:
            needed_count = min(
                get_lack_of_joker(suit_tiles[1:], ucount, needed_count),
                needed_count
            )

        if t1.suit in t1.NUMERIC_SUITS:
            for rank in (1, 2):
                if needed_count == 0:
                    break
                if not t1.validate_mask(t1.mask + rank):
                    continue
                tile = t1 + rank
                ts = suit_tiles[:]
                try:
                    ts.remove(tile)
                except ValueError:
                    continue
                else:
                    needed_count = min(
                        get_lack_of_joker(ts, ucount, needed_count),
                        needed_count
                    )

    if used_count + 2 < needed_count:
        needed_count = min(
            get_lack_of_joker(suit_tiles[:], used_count + 2, needed_count),
            needed_count
        )
    return needed_count
