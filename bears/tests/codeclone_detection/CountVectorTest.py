import sys

sys.path.insert(0, ".")
import unittest
from bears.codeclone_detection.CountVector import CountVector


class CountVectorTest(unittest.TestCase):
    def test_simple_creation(self):
        uut = CountVector("varname")
        self.assertEqual(uut.count_vector, [])
        uut = CountVector("varname", [])
        self.assertEqual(uut.count_vector, [])
        self.assertRaises(AssertionError,
                          CountVector,
                          "varname",
                          [],
                          [2])

    def test_len(self):
        uut = CountVector("varname")
        self.assertEqual(len(uut), 0)

        uut = CountVector("varname", [lambda x: x])
        self.assertEqual(len(uut), 1)

    def test_counting(self):
        uut = CountVector("varname", [lambda cursor, stack: cursor and stack])
        self.assertEqual(uut.count_vector, [0])
        uut.count_reference(True, True)
        self.assertEqual(uut.count_vector, [1])
        uut.count_reference(True, False)
        self.assertEqual(uut.count_vector, [1])

    def test_weighting(self):
        uut = CountVector("varname",
                          [lambda cursor, stack: cursor and stack,
                           lambda cursor, stack: cursor],
                          [2, 1])
        uut.count_reference(True, True)
        self.assertEqual(uut.count_vector, [2, 1])
        uut.count_reference(True, False)
        self.assertEqual(uut.count_vector, [2, 2])

    def test_conversions(self):
        uut = CountVector("varname",
                          [lambda cursor, stack: cursor and stack],
                          [2])
        uut.count_reference(True, True)
        self.assertEqual(repr(uut), str(uut))
        self.assertEqual(repr(uut), "[2]")
        self.assertEqual(list(uut), [2])

    def check_difference(self, cv1, cv2, expected_difference):
        """
        Checks the difference between the given count vectors.

        :param cv1:                 List of counts to put in the first CV.
        :param cv2:                 List of counts to put in the second CV.
        :param expected_difference: The expected difference value.
        """
        # Create empty CountVector objects
        count_vector1 = CountVector("", [lambda: False for i in cv1])
        count_vector2 = CountVector("", [lambda: False for i in cv2])
        # Manually hack in the test values
        count_vector1.count_vector = cv1
        count_vector2.count_vector = cv2

        self.assertEqual(count_vector1.difference(count_vector2),
                         expected_difference,
                         "Difference value for vectors {} and {} doesnt match"
                         ".".format(cv1, cv2))
        self.assertEqual(count_vector2.difference(count_vector1),
                         expected_difference,
                         "The difference operation is not symmetric.")

    def test_difference(self):
        # For each tuple first two items are CVs to compare, third is dif value
        count_vector_difference_matrix = [
            ([], [], 0),
            ([0], [0], 0),
            ([1], [1], 0),
            ([100], [100], 0),

            ([0], [100], 1),
            ([0], [1], 1),
            ([0, 1], [1, 0], 1),

            ([0, 1], [1, 1], 0.5),
            ([0, 2], [1, 2], 0.2),  # Higher values get weighted more
            ([4], [3], 1/16),
            ([0, 4], [0, 3], 1/16)]  # Zeros are weighted zeroly

        for elem in count_vector_difference_matrix:
            self.check_difference(*elem)


if __name__ == '__main__':
    unittest.main(verbosity=2)