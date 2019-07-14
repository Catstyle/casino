from bisect import insort
from collections import Counter

from casino.utils import random_shuffle_algorithm

from .properties import filter_sequence, filter_sequence_2_7_10
from .properties import filter_triplet, filter_triplet_rank


class Manager(object):

    def __init__(self, shuffle_algorithm=None):
        self.shuffle_algorithm = shuffle_algorithm or random_shuffle_algorithm
        self.cards = []
        self.patterns = []
        self.chow_filter = [
            filter_sequence, filter_triplet_rank, filter_sequence_2_7_10
        ]

    def reset(self, cards, ran):
        self.cards = cards
        self.shuffle_algorithm(cards, ran)

    def register_patterns(self, patterns):
        self.patterns.extend(patterns)

    def get_pattern(self, handcard):
        cards = handcard.cards
        combinations = self.get_combinations(cards)
        handcard.used_combs = []
        handcard.combinations = combinations
        for pattern in self.patterns:
            if pattern.validate(handcard, combinations, {}):
                return pattern

    def get_pattern_with_card(self, handcard, card, separate=True):
        cards = handcard.cards
        if not separate and cards.count(card) == 2:
            cards.remove(card)
            cards.remove(card)
            handcard.fixed_cards[card] = 3
        else:
            insort(cards, card)
        pattern = self.get_pattern(handcard)
        if not separate and card not in cards:
            insort(cards, card)
            insort(cards, card)
            handcard.fixed_cards.pop(card)
        else:
            cards.remove(card)
        return pattern

    def check_win(self, handcard):
        cards = handcard.cards[:]
        count = len(cards)
        if count % 3 not in {2, 0}:
            return False

        if count == 2 and cards[0] is cards[1]:
            return True

        if count == 0 and (handcard.fixed_cards or handcard.used_cards):
            return True

        return any(self.combinations(cards))

    def check_win_with_card(self, handcard, card, separate=True):
        handcard = handcard.clone()
        cards = handcard.cards
        insort(cards, card)
        if not separate and cards.count(card) == 3:
            cards.remove(card)
            cards.remove(card)
            cards.remove(card)
            handcard.fixed_cards[card] = 3
        return self.check_win(handcard)

    def has_candidates(self, cards):
        # if it has candidates, give it a joker, should have combinations
        return any(self.combinations(cards, 1))

    def check_chow(self, handcard, card):
        cards = handcard.cards[:]
        insort(cards, card)
        return list(self._check_chow(cards, card))

    def _check_chow(self, cards, card):
        if len(cards) <= 2:
            return
        for comb_filter in self.chow_filter:
            for comb, _ in comb_filter(cards, card):
                cs = cards[:]
                for c in comb:
                    cs.remove(c)
                if cs.count(card) > 0:
                    for next_comb in self._check_chow(cs, card):
                        yield comb + next_comb
                else:
                    yield comb

    def check_pong(self, handcard, card):
        return handcard.cards.count(card) == 2

    # pao pai
    def check_exposed_kong(self, handcard, card, with_pong=True):
        if handcard.fixed_cards[card] == 3:
            return True

        pongs = handcard.used_cards['concealed_pong']
        if with_pong:
            pongs = pongs + handcard.used_cards['pong']
        return any(pong[0] is card for pong in pongs)

    # ti pai
    def check_concealed_kong(self, handcard, card):
        # card donot put in handcard
        return (
            handcard.fixed_cards[card] == 3 or
            any(card in ep for ep in handcard.used_cards['concealed_pong'])
        )

    def check_chow_cards(self, cards):
        if len(cards) % 3 != 0:
            return False
        idx = 0
        while idx < len(cards):
            comb = cards[idx:idx + 3]
            idx += 3
            if not any(
                any(comb_filter(comb, comb[2]))
                for comb_filter in self.chow_filter
            ):
                return False
        return True

    def chow(self, handcard, cards):
        available_cards = handcard.cards
        for chow_card in cards:
            available_cards.remove(chow_card)

        handcard.used_cards['chow'].append(cards[:])

    def pong(self, handcard, card):
        cards = handcard.cards
        idx = cards.index(card)
        cards[idx:idx + 2] = []
        assert cards.count(card) < 2, cards
        handcard.used_cards['pong'].append([card, card, card])

    def concealed_pong(self, handcard, card):
        cards = handcard.cards
        idx = cards.index(card)
        cards[idx:idx + 2] = []
        assert cards.count(card) < 2, cards
        handcard.used_cards['concealed_pong'].append([card, card, card])

    def exposed_kong(self, handcard, card):
        cards = handcard.fixed_cards
        used_cards = handcard.used_cards

        if card in cards:
            assert cards[card] == 3, cards
            cards.pop(card)
            count = 3
        else:
            removing = [card, card, card]
            if removing in used_cards['concealed_pong']:
                used_cards['concealed_pong'].remove(removing)
            elif removing in used_cards['pong']:
                used_cards['pong'].remove(removing)
            else:
                assert False, (removing, handcard)
            count = 1
        handcard.used_cards['exposed_kong'].append([card, card, card, card])
        return count

    def concealed_kong(self, handcard, card):
        cards = handcard.fixed_cards
        used_cards = handcard.used_cards

        if card in cards:
            assert cards[card] == 3, cards
            cards.pop(card)
            count = 3
        else:
            assert [card, card, card] in used_cards['concealed_pong'], \
                ([card, card, card], used_cards['concealed_pong'])
            used_cards['concealed_pong'].remove([card, card, card])
            count = 1
        used_cards['concealed_kong'].append([card, card, card, card])
        return count

    def sub_combinations(self, cards, joker_count=0):
        # only need to check chow_filter
        count = len(cards)
        if count == 0:
            return

        if (count + joker_count) % 3 != 0:
            return

        card = cards[0]
        combinations = self.sub_combinations
        for comb_filter in self.chow_filter:
            for comb, used_joker in comb_filter(cards, card, joker_count):
                cs = cards[:]
                for c in comb:
                    cs.remove(c)
                if not cs:
                    yield {'triplets': [], 'sequences': [comb]}
                    continue

                for next_comb in combinations(cs, joker_count - used_joker):
                    next_comb['sequences'] = [comb] + next_comb['sequences']
                    yield next_comb

        for comb, used_joker in filter_triplet(cards, card, joker_count):
            cs = cards[:]
            for c in comb:
                cs.remove(c)
            if not cs:
                yield {'triplets': [comb], 'sequences': []}
                continue

            for next_comb in combinations(cs, joker_count - used_joker):
                next_comb['triplets'] = [comb] + next_comb['triplets']
                yield next_comb

    def combinations_with_eye(self, cards, joker_count=0):
        for eye, count in Counter(cards).items():
            if count >= 2:
                cs = cards[:]
                cs.remove(eye)
                cs.remove(eye)
                if cs:
                    for comb in self.sub_combinations(cs, joker_count):
                        comb['eye'] = [eye, eye]
                        yield comb
                else:
                    yield {'eye': [eye, eye], 'triplets': [], 'sequences': []}
            if joker_count == 1:
                cs = cards[:]
                cs.remove(eye)
                if cs:
                    for comb in self.sub_combinations(cs, joker_count - 1):
                        comb['eye'] = [eye]
                        yield comb
                else:
                    yield {'eye': [eye], 'triplets': [], 'sequences': []}

    def combinations(self, cards, joker_count=0):
        count = len(cards)
        if (count + joker_count) % 3 == 2:
            for comb in self.combinations_with_eye(cards, joker_count):
                yield comb
        elif count:
            for comb in self.sub_combinations(cards, joker_count):
                comb['eye'] = []
                yield comb

    def get_combinations(self, cards):
        return list(self.combinations(cards))
