from unittest import TestCase

from casino.wordplate import Card
from casino.wordplate.properties import (
    filter_sequence, filter_triplet, filter_triplet_rank,
    filter_sequence_2_7_10, filter_sequence_1_5_10,
)

l1 = Card.LOWER_ONE
l2 = Card.LOWER_TWO
l3 = Card.LOWER_THREE
l4 = Card.LOWER_FOUR
l5 = Card.LOWER_FIVE
l6 = Card.LOWER_SIX
l7 = Card.LOWER_SEVEN
l10 = Card.LOWER_TEN

u2 = Card.UPPER_TWO
u3 = Card.UPPER_THREE


class PropertiesTest(TestCase):

    def test_filter_sequence(self):
        self.assertListEqual(
            list(filter_sequence([l3, l4, l5], l3)), [([l3, l4, l5], 0)],
        )
        self.assertListEqual(
            list(filter_sequence([l3, l4, l5, l6], l4)),
            [([l3, l4, l5], 0), ([l4, l5, l6], 0)],
        )
        self.assertListEqual(list(filter_sequence([l3, l4], l3)), [])
        self.assertListEqual(list(filter_sequence([], l3)), [])
        self.assertListEqual(
            list(filter_sequence([u3, l4, l5], l4)), [],
        )

        self.assertListEqual(
            list(filter_sequence([l3, l5], l3, 1)), [([l3, l5], 1)],
        )
        self.assertListEqual(
            list(filter_sequence([l3, l4, l6], l4, 1)),
            [([l3, l4], 1), ([l4, l6], 1)],
        )

    def test_filter_triplet(self):
        self.assertListEqual(
            list(filter_triplet([l3, l3, l3], l3)), [([l3, l3, l3], 0)],
        )
        self.assertListEqual(
            list(filter_triplet([u3, u3, u3], u3)), [([u3, u3, u3], 0)],
        )
        self.assertListEqual(
            list(filter_triplet([l3, l3, l3, u3], l3)), [([l3, l3, l3], 0)],
        )
        self.assertListEqual(list(filter_triplet([l3, l3, u3], l3)), [])
        self.assertListEqual(list(filter_triplet([l3, l3], l3)), [])

        self.assertListEqual(
            list(filter_triplet([l3, l3], l3, 1)), [([l3, l3], 1)],
        )

    def test_filter_triplet_rank(self):
        self.assertListEqual(
            list(filter_triplet_rank([l3, l3, u3], l3)), [([l3, l3, u3], 0)],
        )
        self.assertListEqual(
            list(filter_triplet_rank([l3, u3, u3], l3)), [([l3, u3, u3], 0)],
        )
        self.assertListEqual(
            list(filter_triplet_rank([l3, l3, u3, u3], l3)),
            [([l3, l3, u3], 0), ([l3, u3, u3], 0)],
        )
        self.assertListEqual(list(filter_triplet_rank([l3, l3, l3], l3)), [])
        self.assertListEqual(list(filter_triplet_rank([l3, l3], l3)), [])

        self.assertListEqual(
            list(filter_triplet_rank([l3, l3], l3, 1)), [([l3, l3], 1)],
        )
        self.assertListEqual(
            list(filter_triplet_rank([l3, u3], l3, 1)), [([l3, u3], 1)],
        )

    def test_filter_sequence_2_7_10(self):
        self.assertListEqual(
            list(filter_sequence_2_7_10([l2, l7, l10], l2)),
            [([l2, l7, l10], 0)],
        )
        self.assertListEqual(
            list(filter_sequence_2_7_10([u2, l7, l10], u2)), [],
        )
        self.assertListEqual(
            list(filter_sequence_2_7_10([l3, l7, l10], l7)), [],
        )

        self.assertListEqual(
            list(filter_sequence_2_7_10([l2, l10], l2, 1)),
            [([l2, l10], 1)],
        )

    def test_filter_sequence_1_5_10(self):
        self.assertListEqual(
            list(filter_sequence_1_5_10([l1, l5, l10], l1)),
            [([l1, l5, l10], 0)],
        )
        self.assertListEqual(
            list(filter_sequence_1_5_10([Card.UPPER_ONE, l5, l10], l5)), [],
        )
        self.assertListEqual(
            list(filter_sequence_1_5_10([l2, l5, l10], l5)), [],
        )

        self.assertListEqual(
            list(filter_sequence_1_5_10([l1, l10], l1, 1)),
            [([l1, l10], 1)],
        )
