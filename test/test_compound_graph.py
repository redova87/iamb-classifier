import unittest
from pprint import pprint, pformat
from iambic_line_processors.combinations_graph import CombinationsGraph
from iambic_line_processors.demote_combinations_graph import DemoteCombinationsGraph

unittest.TestCase.maxDiff=None

def equal(expected, actual):
    msg = "'" + pformat(actual) + "' != '" + pformat(expected) + "'"
    assert expected == actual, msg



class TestCombinationsGraph(unittest.TestCase):


    def test_single_two_slots(self):
        cg = CombinationsGraph([([1], [0, 1, 0, 0, 2], [1], [1], [1], [1])])
        self.assertEqual(cg.new_combinations, [
            ([1], [0, 1, 0, 0, 2], [1], [1], [1], [1]),
            ([1], [0, 1, 2, 0, 2], [1], [1], [1], [1]),
            ([1], [2, 1, 0, 0, 2], [1], [1], [1], [1]),
            ([1], [2, 1, 2, 0, 2], [1], [1], [1], [1])
        ])

    def test_one_slot(self):
        cg = CombinationsGraph([
            ([0], [0], [0], [1], [1, 1], [0, 1, 0, 0]),
            ])
        equal(cg.new_combinations, [
            ([0], [0], [0], [1], [1, 1], [0, 1, 0, 0]),
            ([0], [0], [0], [1], [1, 1], [0, 1, 0, 2]),
        ])




        ([0], [0], [0], [1], [1, 0], [0, 1, 0, 0])

        # ([1], [0, 1, 2, 0, 2], [1], [1], [1, 2]),


class TestDemoteCombinationsGraph(unittest.TestCase):


    def test_single_two_slots(self):
        dcg = DemoteCombinationsGraph([
            ([1], [0, 1, 2, 0, 2], [1], [1], [1, 2])
            ])

        equal(dcg.new_combinations, [
            ([1], [0, 2, 2, 0, 2], [1], [1], [2, 2]),
            ([1], [0, 2, 2, 0, 2], [1], [1], [1, 2]),
            ([1], [0, 1, 2, 0, 2], [1], [1], [2, 2]),
            ([1], [0, 1, 2, 0, 2], [1], [1], [1, 2])
        ])


    def test_one_slot(self):
        dcg = DemoteCombinationsGraph([
            ([0], [0], [0], [1], [1, 0], [0, 1, 0, 0]),
            ])
        equal(dcg.new_combinations, [
            ([0], [0], [0], [1], [2, 0], [0, 1, 0, 0]),
            ([0], [0], [0], [1], [1, 0], [0, 1, 0, 0])
        ])


    def test_two_words(self):
        dcg = DemoteCombinationsGraph([
            ([0], [0], [0], [1], [1, 0], [1, 0, 0, 0]),
            ])
        equal(dcg.new_combinations, [
            ([0], [0], [0], [1], [2, 0], [2, 0, 0, 0]),
            ([0], [0], [0], [1], [2, 0], [1, 0, 0, 0]),
            ([0], [0], [0], [1], [1, 0], [2, 0, 0, 0]),
            ([0], [0], [0], [1], [1, 0], [1, 0, 0, 0])
        ])




if __name__ == "__main__":
    unittest.main()