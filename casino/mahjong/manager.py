from collections import namedtuple, defaultdict, Counter
from bisect import insort
from operator import attrgetter

from casino.exceptions import InvalidInstance
from casino.utils import random_shuffle_algorithm

from .patterns import Pairs
from .properties import (
    is_7_pairs, is_7_pairs_with_joker, is_same_suit, get_lack_of_joker,
    combinations
)
from .tile import Tile
from .deck import Deck


Wall = namedtuple(
    'Wall',
    ['all_tiles', 'available_tiles', 'used_tiles', 'suits', 'used_combs']
)
Property = namedtuple(
    'Property', ['same_suit', 'pairs', 'count', 'joker_count', 'jokers']
)


class MahjongManager(object):

    sort_func = attrgetter('priority')

    def __init__(self, shuffle_algorithm=None, tile_class=Tile):
        self.deck = Deck([])
        self.tile_class = tile_class
        self.patterns = []
        self.has_pairs_patterns = False
        self.draw_joker = None
        self.draw_joker_mask = 0
        self.jokers = set()
        self.joker_masks = [0]
        self.joker_factory = None

        self.shuffle_algorithm = shuffle_algorithm or random_shuffle_algorithm
        self._use_normal_api()

    @property
    def left_tiles(self):
        return len(self.deck)

    def _use_normal_api(self):
        self.check_win = self._check_win
        self.check_win_by_tile = self._check_win_by_tile
        self.get_pattern = self._get_pattern
        self.get_pattern_by_tile = self._get_pattern_by_tile
        self.get_candidates = self._get_candidates
        self.has_candidates = self._has_candidates

    def _use_joker_api(self):
        self.check_win = self._check_win_with_joker
        self.check_win_by_tile = self._check_win_by_tile_with_joker
        self.get_pattern = self._get_pattern_with_joker
        self.get_pattern_by_tile = self._get_pattern_by_tile_with_joker
        self.get_candidates = self._get_candidates_with_joker
        self.has_candidates = self._has_candidates_with_joker

    def _check_win(self, tiles, joker_count=0):
        count = len(tiles)
        if count % 3 != 2:
            return False

        if count == 2 and tiles[0] is tiles[1]:
            return True

        return (self.has_pairs_patterns and
                is_7_pairs(tiles) or
                any(combinations(tiles)))

    def _check_win_by_tile(self, tiles, tile):
        tiles = tiles[:]
        insort(tiles, tile)
        return self._check_win(tiles)

    def _check_win_with_joker(self, tiles, joker_count=None):
        count = len(tiles)
        if count % 3 != 2:
            return False

        jokers = self.jokers
        if joker_count is None:
            joker_count = sum(tiles.count(t) for t in jokers)

        if count == 2 and (tiles[0] is tiles[1] or joker_count):
            return True

        tiles = self._filter_joker_tiles(tiles, joker_count)
        return (self.has_pairs_patterns and
                is_7_pairs_with_joker(tiles, joker_count) or
                any(combinations(tiles, joker_count)))

    def _check_win_by_tile_with_joker(self, tiles, tile, joker_count=None):
        if joker_count is None:
            joker_count = sum(tiles.count(t) for t in self.jokers)
        tiles = tiles[:]
        insort(tiles, tile)
        return self._check_win_with_joker(tiles, joker_count)

    def _get_pattern(self, tile_wall, joker_count=0):
        tiles = tile_wall.available_tiles
        combinations = self.get_combinations(tiles, 0, tile_wall.used_tiles)
        tile_wall.used_combs = []
        tile_wall.combinations = combinations
        properties = Property(
            is_same_suit(tile_wall.all_tiles),
            is_7_pairs(tiles),
            tile_wall.available_count,
            0,
            {},
        )
        for pattern in self.patterns:
            if pattern.validate(tile_wall, combinations, properties):
                return pattern

    def _get_pattern_by_tile(self, tile_wall, tile, joker_count=0):
        tile_wall.add_tile(tile)
        pattern = self._get_pattern(tile_wall)
        tile_wall.remove_tile(tile)
        return pattern

    def _get_pattern_with_joker(self, tile_wall, joker_count=None):
        jokers = self.jokers
        available_tiles = tile_wall.available_tiles
        if joker_count is None:
            joker_count = sum(available_tiles.count(joker) for joker in jokers)

        all_tiles = self._filter_joker_tiles(tile_wall.all_tiles, joker_count)
        tiles = self._filter_joker_tiles(available_tiles, joker_count)
        used_tiles = tile_wall.used_tiles
        combinations = self.get_combinations(tiles, joker_count, used_tiles)

        tile_wall.used_combs = []
        tile_wall.combinations = combinations
        wall = Wall(
            all_tiles, tiles, used_tiles, tile_wall.suits, tile_wall.used_combs
        )
        properties = Property(
            is_same_suit(all_tiles),
            is_7_pairs_with_joker(tiles, joker_count),
            tile_wall.available_count,
            joker_count,
            jokers,
        )
        for pattern in self.patterns:
            if pattern.validate(wall, combinations, properties):
                return pattern

    def _get_pattern_by_tile_with_joker(self, tile_wall, tile,
                                        joker_count=None):
        if joker_count is None:
            joker_count = sum(
                tile_wall.available_tiles.count(joker) for joker in self.jokers
            )
        tile_wall.add_tile(tile)
        pattern = self._get_pattern_with_joker(tile_wall, joker_count)
        tile_wall.remove_tile(tile)
        return pattern

    def _filter_joker_tiles(self, tiles, joker_count):
        subcount = 0
        filtered_tiles = []
        for tile in tiles:
            if tile in self.jokers and subcount < joker_count:
                subcount += 1
            else:
                filtered_tiles.append(tile)
        return filtered_tiles

    def _get_candidates(self, tiles, joker_count=0):
        if (len(tiles) + joker_count) % 3 == 1:
            tile_set = set()
            if (self.has_pairs_patterns and
                    is_7_pairs_with_joker(tiles, joker_count + 1)):
                idx = 0
                count = len(tiles)
                jc = joker_count
                while idx < count and joker_count >= 0:
                    if idx + 1 == count:
                        jc -= 1
                        tile_set.add(tiles[idx])
                        break
                    elif tiles[idx] is tiles[idx + 1]:
                        idx += 2
                    else:
                        tile_set.add(tiles[idx])
                        jc -= 1
                        idx += 1
                if jc > 0:
                    for cand in self.deck.tile_set:
                        yield cand
                    return

            tile_class = self.tile_class
            for comb in combinations(tiles, joker_count + 1):
                if comb['joker_count'] > 0:
                    tile_set = self.deck.tile_set
                    break

                if len(comb['eye']) == 1:
                    tile_set.add(comb['eye'][0])
                elif len(comb['eye']) == 0:
                    tile_set = self.deck.tile_set
                    break

                for trip in comb['triplets']:
                    if len(trip) != 3:
                        tile_set.add(trip[0])

                for seq in comb['sequences']:
                    if len(seq) == 2:
                        if seq[1].rank - seq[0].rank == 1:
                            mask = seq[0].mask
                            for delta in (-1, 2):
                                try:
                                    tile_set.add(
                                        tile_class.from_mask(mask + delta)
                                    )
                                except InvalidInstance:
                                    pass
                        else:
                            # gap
                            tile_set.add(
                                tile_class.from_mask(seq[0].mask + 1)
                            )
                    elif len(seq) == 1:
                        mask = seq[0].mask
                        for delta in (-2, -1, 1, 2):
                            try:
                                tile_set.add(
                                    tile_class.from_mask(mask - delta)
                                )
                            except InvalidInstance:
                                pass

            for cand in tile_set:
                yield cand

    def _get_candidates_with_joker(self, tiles, joker_count=None):
        if len(tiles) % 3 == 1:
            if joker_count is None:
                joker_count = self.get_joker_count(tiles)
            tiles = self._filter_joker_tiles(tiles, joker_count)
            for cand in self._get_candidates(tiles, joker_count):
                yield cand

    def _has_candidates(self, tiles, joker_count=0):
        # if it has candidates, give it a joker, should have combinations
        return (self.has_pairs_patterns and is_7_pairs_with_joker(tiles, 1) or
                any(combinations(tiles, 1)))

    def _has_candidates_with_joker(self, tiles, joker_count=None):
        # if it has candidates, give it a more joker, should have combinations
        if joker_count is None:
            joker_count = self.get_joker_count(tiles)
        tiles = self._filter_joker_tiles(tiles, joker_count)
        return (
            self.has_pairs_patterns and
            is_7_pairs_with_joker(tiles, joker_count + 1) or
            any(combinations(tiles, joker_count + 1))
        )

    def set_joker_factory(self, joker_factory):
        self.joker_factory = joker_factory
        self._use_joker_api()

    def reset(self, deck, ran):
        self.draw_joker = None
        self.jokers.clear()

        self.deck = deck
        self.shuffle_algorithm(deck.tiles, ran)

        if self.joker_factory:
            draw_joker, jokers = self.joker_factory(deck)
            self.draw_joker, self.draw_joker_mask = draw_joker, draw_joker.mask
            self.jokers = set(jokers)
            self.joker_masks = [tile.mask for tile in jokers]

    def register_pattern(self, pattern, sort_func=None):
        self.patterns.append(pattern)
        self.patterns.sort(key=sort_func or self.sort_func, reverse=True)
        if issubclass(pattern, Pairs):
            self.has_pairs_patterns = True

    def register_patterns(self, patterns, sort_func=None):
        self.patterns.extend(patterns)
        self.patterns.sort(key=sort_func or self.sort_func, reverse=True)
        self.has_pairs_patterns = any(
            issubclass(p, Pairs) for p in self.patterns
        )

    def check_exposed_kong(self, wall, tile):
        return wall.available_tiles.count(tile) == 3

    def check_concealed_kong(self, wall, tile):
        return wall.available_tiles.count(tile) == 4

    def check_additional_kong(self, wall, tile):
        return wall.available_tiles.count(tile) == 1 and \
            tile in {tiles[0] for tiles in wall.used_tiles['pong']}

    def get_concealed_kong_tiles(self, wall):
        counter = Counter(wall.available_tiles)
        return [tile for tile, count in counter.items() if count == 4]

    def get_additional_kong_tiles(self, wall):
        pong_tiles = {tiles[0] for tiles in wall.used_tiles['pong']}
        available_tiles = wall.available_tiles
        return [tile for tile in pong_tiles if tile in available_tiles]

    def check_pong_tile(self, wall, tile):
        return wall.available_tiles.count(tile) >= 2

    def check_chow_tile(self, wall, tile):
        if tile.suit not in self.tile_class.NUMERIC_SUITS:
            return False
        available_tiles = wall.available_tiles
        for combs in ((1, 2), (-1, 1), (-2, -1)):
            try:
                if all(tile + rank in available_tiles for rank in combs):
                    return True
            except InvalidInstance:
                continue
        return False

    def check_chow_tiles(self, tiles, tile):
        if len(tiles) != 2:
            return False
        tiles = sorted(tiles + [tile])
        last_suit, last_rank = tiles[0].suit, tiles[0].rank - 1
        for tile in tiles:
            if tile.suit not in self.tile_class.NUMERIC_SUITS:
                return False
            if tile.suit != last_suit or tile.rank - last_rank != 1:
                return False
            last_rank = tile.rank
        return True

    def chow(self, wall, tiles, tile):
        available_tiles = wall.available_tiles
        for chow_tile in tiles:
            available_tiles.remove(chow_tile)

        wall.used_tiles['chow'].append(sorted(tiles + [tile]))
        wall.used_count += 3
        wall.suits[tile.suit] += 1

    def pong(self, wall, tile):
        available_tiles = wall.available_tiles
        idx = available_tiles.index(tile)
        available_tiles[idx:idx + 2] = []
        assert available_tiles.count(tile) < 2, available_tiles
        wall.used_tiles['pong'].append([tile, tile, tile])
        wall.used_count += 3
        wall.suits[tile.suit] += 1

    def exposed_kong(self, wall, tile):
        available_tiles = wall.available_tiles
        assert available_tiles.count(tile) == 3, (tile, available_tiles)

        idx = available_tiles.index(tile)
        available_tiles[idx:idx + 3] = []
        assert available_tiles.count(tile) == 0, available_tiles.count(tile)
        wall.used_tiles['kong']['exposed'].append([tile, tile, tile, tile])
        wall.used_count += 4
        wall.suits[tile.suit] += 1

    def concealed_kong(self, wall, tile):
        available_tiles = wall.available_tiles
        assert available_tiles.count(tile) == 4, (tile, available_tiles)

        idx = available_tiles.index(tile)
        available_tiles[idx:idx + 4] = []
        assert available_tiles.count(tile) == 0, available_tiles
        wall.used_tiles['kong']['concealed'].append([tile, tile, tile, tile])
        wall.used_count += 4

    def additional_kong(self, wall, tile):
        wall.available_tiles.remove(tile)
        assert wall.available_tiles.count(tile) == 0, wall.available_tiles

        used_tiles = wall.used_tiles
        used_tiles['pong'].remove([tile, tile, tile])
        used_tiles['kong']['additional'].append([tile, tile, tile, tile])
        wall.used_count += 1

    def get_combinations(self, tiles, joker_count=0, used_tiles=None):
        results = []
        if used_tiles:
            kongs = sum(used_tiles['kong'].values(), [])
        for comb in combinations(tiles, joker_count):
            if used_tiles:
                comb['sequences'].extend(used_tiles['chow'])
                comb['triplets'].extend(used_tiles['pong'])
                comb['quaternion'] = kongs
            results.append(comb)
        return results

    def get_joker_count(self, tiles):
        return sum(tiles.count(joker) for joker in self.jokers)

    def get_joker_tiles(self, tiles):
        return [tile for tile in tiles if tile in self.jokers]

    def filter_joker_tiles(self, tiles):
        return [tile for tile in tiles if tile not in self.jokers]

    def has_free_joker(self, tiles, joker_count=None):
        if len(tiles) % 3 == 1:
            if joker_count is None:
                joker_count = self.get_joker_count(tiles)
            filtered_tiles = self._filter_joker_tiles(tiles, joker_count)
            suits = defaultdict(list)
            for tile in filtered_tiles:
                suits[tile.suit].append(tile)
            lack_of_joker = {
                suit: get_lack_of_joker(suits[suit]) for suit in suits
            }
            return joker_count > sum(lack_of_joker.values())
        return False
