import unittest
from rook import Rook


class TestRook(unittest.TestCase):
    def setUp(self):
        self._rook = Rook()

    def test_next_valid_positions(self):
        expected_positions = [[('a%s' % z) for z in range(2, 9)], [
            ('%s1' % i) for i in 'bcdefgh']]
        actual_positions = [str(p)
                            for p in self._rook.next_valid_positions()]

        for ap in actual_positions:
            self.assertTrue(
                ap in expected_positions[0] or ap in expected_positions[1])

        self.assertEqual(len(actual_positions), len(
            expected_positions[0]) + len(expected_positions[1]))


if __name__ == '__main__':
    unittest.main()
