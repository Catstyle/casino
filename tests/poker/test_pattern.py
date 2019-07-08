from unittest import TestCase

from casino.poker import Card
from casino.poker.patterns import Pair, Pairs, Triplet, Triplets
from casino.poker.properties import get_properties

d3 = Card.DIAMOND_THREE
d4 = Card.DIAMOND_FOUR
d5 = Card.DIAMOND_FIVE
d6 = Card.DIAMOND_SIX

c3 = Card.CLUB_THREE
c4 = Card.CLUB_FOUR
c5 = Card.CLUB_FIVE

dj = Card.DIAMOND_JACK
dq = Card.DIAMOND_QUEEN
dk = Card.DIAMOND_KING
da = Card.DIAMOND_ACE
d2 = Card.DIAMOND_TWO


class PatternTest(TestCase):

    def test_pair(self):
        self.assertTrue(Pair.validate(get_properties([d3, d3])))
        self.assertTrue(Pair.validate(get_properties([d3, c3])))
        self.assertFalse(Pair.validate(get_properties([d3, d4])))
        self.assertFalse(Pair.validate(get_properties([d3])))
        self.assertFalse(Pair.validate(get_properties([d3, d3, d3])))

        self.assertEqual(
            Pair(get_properties([d3, d3])), Pair(get_properties([d3, d3]))
        )
        self.assertEqual(
            Pair(get_properties([d3, d3])), Pair(get_properties([d3, c3]))
        )

        self.assertNotEqual(
            Pair(get_properties([d3, d3])), Pair(get_properties([d4, c4]))
        )
        self.assertGreaterEqual(
            Pair(get_properties([d4, d4])), Pair(get_properties([d3, c3]))
        )
        self.assertLessEqual(
            Pair(get_properties([d3, d3])), Pair(get_properties([d4, c4]))
        )

        self.assertListEqual(
            list(Pair.filter(get_properties([d4, c4]), d3)), [d4, c4]
        )
        self.assertListEqual(
            list(Pair.filter(get_properties([d3, c3]), d3)), []
        )
        self.assertListEqual(
            list(Pair.filter(get_properties([d3, c4]), d3)), []
        )
        self.assertListEqual(
            list(Pair.filter(get_properties([]), d3)), []
        )
        self.assertListEqual(
            list(Pair.filter(get_properties([d4, c4, c4]), d3)), []
        )
        self.assertListEqual(
            list(Pair.filter(get_properties([d4, c4, c4]), d3, force=True)),
            [d4, c4]
        )

    def test_pairs(self):
        self.assertTrue(
            Pairs.validate(get_properties([d3, d3, d4, d4, d5, d5]))
        )
        self.assertTrue(
            Pairs.validate(get_properties([d3, d3, d4, d4, d5, d5]))
        )
        self.assertTrue(
            Pairs.validate(get_properties([d3, d4, d5, c3, c4, c5]))
        )

        self.assertFalse(
            Pairs.validate(get_properties([d3, d3, d4, d4, dj, dj]))
        )
        self.assertFalse(Pairs.validate(get_properties([d3, d3, d4, d4])))
        self.assertFalse(
            Pairs.validate(get_properties([d3, d3, d4, d4, d4, d5]))
        )

        self.assertTrue(
            Pairs.validate(get_properties([dq, dq, dk, dk, da, da]))
        )
        self.assertFalse(
            Pairs.validate(get_properties([dk, dk, da, da, d2, d2]))
        )

        cards = [d3, d3, d4, d4, d5, d5]
        self.assertEqual(
            Pairs(get_properties(cards)), Pairs(get_properties(cards))
        )

        cards = [d3, d3, d4, c4, d5, c5]
        self.assertEqual(
            Pairs(get_properties(cards)), Pairs(get_properties(cards))
        )

        self.assertNotEqual(
            Pairs(get_properties([d3, d3, d4, d4, d5, d5])),
            Pairs(get_properties([d4, c4, d5, d5, d6, d6]))
        )
        self.assertLessEqual(
            Pairs(get_properties([d3, d3, d4, d4, d5, d5])),
            Pairs(get_properties([d4, c4, d5, d5, d6, d6]))
        )
        self.assertGreaterEqual(
            Pairs(get_properties([d4, c4, d5, d5, d6, d6])),
            Pairs(get_properties([d3, d3, d4, d4, d5, d5]))
        )

        self.assertListEqual(
            list(Pairs.filter(get_properties([d4, d4, d5, d5, d6, d6]), d5)),
            [d4, d4, d5, d5, d6, d6]
        )
        self.assertListEqual(
            list(Pairs.filter(get_properties([d3, d3, d4, d4, d5, d5]), d5)),
            []
        )
        self.assertListEqual(
            list(Pairs.filter(get_properties([d3, d3, d4, d4, d5, d6]), d5)),
            []
        )
        self.assertListEqual(
            list(Pairs.filter(get_properties([d3, d3, d4, d4, d5]), d5)),
            []
        )
        self.assertListEqual(
            list(Pairs.filter(get_properties([d4, d4, d5, d5, d5, d6, d6]),
                              d5)),
            []
        )
        self.assertListEqual(
            list(Pairs.filter(get_properties([d4, d4, d5, d5, d5, d6, d6]),
                              d5, force=True)),
            [d4, d4, d5, d5, d6, d6]
        )

    def test_triplet(self):
        self.assertTrue(Triplet.validate(get_properties([d3, d3, d3])))
        self.assertTrue(Triplet.validate(get_properties([d3, d3, c3])))
        self.assertFalse(Triplet.validate(get_properties([d3, d3, d4])))
        self.assertFalse(Triplet.validate(get_properties([d3, d3])))
        self.assertFalse(Triplet.validate(get_properties([d3, d3, d3, d3])))

        self.assertEqual(
            Triplet(get_properties([d3, d3, d3])),
            Triplet(get_properties([d3, d3, d3]))
        )
        self.assertEqual(
            Triplet(get_properties([d3, d3, d3])),
            Triplet(get_properties([d3, d3, c3]))
        )

        self.assertNotEqual(
            Triplet(get_properties([d3, d3, d3])),
            Triplet(get_properties([d4, d4, c4]))
        )
        self.assertGreaterEqual(
            Triplet(get_properties([d4, d4, d4])),
            Triplet(get_properties([d3, d3, d3]))
        )
        self.assertLessEqual(
            Triplet(get_properties([d3, d3, d3])),
            Triplet(get_properties([d4, d4, c4]))
        )

        self.assertListEqual(
            list(Triplet.filter(get_properties([d4, d4, c4]), d3)),
            [d4, d4, c4]
        )
        self.assertListEqual(
            list(Triplet.filter(get_properties([d3, d3, c3]), d3)), []
        )
        self.assertListEqual(
            list(Triplet.filter(get_properties([d3, d3, c4]), d3)), []
        )
        self.assertListEqual(
            list(Triplet.filter(get_properties([]), d3)), []
        )
        self.assertListEqual(
            list(Triplet.filter(get_properties([d4, d4, c4, c4]), d3)), []
        )
        self.assertListEqual(
            list(Triplet.filter(get_properties([d4, d4, c4, c4]), d3,
                                force=True)),
            [d4, d4, c4]
        )

    def test_triplets(self):
        self.assertTrue(
            Triplets.validate(get_properties([d3, d3, d3, d4, d4, d4]))
        )
        self.assertTrue(
            Triplets.validate(get_properties([d3, d3, c3, d4, d4, c4]))
        )
        self.assertTrue(
            Triplets.validate(get_properties([d3, d3, d4, c3, c4, c4]))
        )
        self.assertFalse(
            Triplets.validate(get_properties([d3, d3, d3, d5, d5, d5]))
        )
        self.assertFalse(
            Triplets.validate(get_properties([d3, d3, d3, d4, d4]))
        )
        self.assertFalse(
            Triplets.validate(get_properties([d3, d3, d3, d4, d4, d4, d5]))
        )

        self.assertTrue(
            Triplets.validate(get_properties([dk, dk, dk, da, da, da]))
        )
        self.assertFalse(
            Triplets.validate(get_properties([da, da, da, d2, d2, d2]))
        )

        self.assertEqual(
            Triplets(get_properties([d3, d3, d3, d4, d4, d4])),
            Triplets(get_properties([d3, d3, d3, d4, d4, d4]))
        )
        self.assertEqual(
            Triplets(get_properties([d3, d3, d3, d4, d4, d4])),
            Triplets(get_properties([d3, c3, d3, c4, d4, c4]))
        )

        self.assertNotEqual(
            Triplets(get_properties([d3, d3, d3, d4, d4, d4])),
            Triplets(get_properties([d4, c4, d4, d5, d5, d5]))
        )
        self.assertLessEqual(
            Triplets(get_properties([d3, d3, d3, d4, d4, d4])),
            Triplets(get_properties([d4, c4, d4, d5, d5, d5]))
        )
        self.assertGreaterEqual(
            Triplets(get_properties([d4, c4, d4, d5, d5, d5])),
            Triplets(get_properties([d3, d3, d3, d4, d4, d4]))
        )

        self.assertListEqual(
            list(Triplets.filter(get_properties([d4, d4, c4, d5, d5, c5]),
                                 d4)),
            [d4, d4, c4, d5, d5, c5]
        )
        self.assertListEqual(
            list(Triplets.filter(get_properties([d3, d3, c3, d4, d4, c4]),
                                 d4)),
            []
        )
        self.assertListEqual(
            list(Triplets.filter(get_properties([d4, d4, c4, d5, d5]), d4)), []
        )
        self.assertListEqual(
            list(Triplet.filter(get_properties([]), d4)), []
        )
        self.assertListEqual(
            list(Triplets.filter(get_properties([d4, d4, c4, c4, d5, d5, c5]),
                                 d4)),
            []
        )
        self.assertListEqual(
            list(Triplets.filter(get_properties([d4, d4, c4, c4, d5, d5, c5]),
                                 d4, force=True)),
            [d4, d4, c4, d5, d5, c5]
        )
