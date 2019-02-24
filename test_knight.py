import unittest
from knight import Knight


class TestKnight(unittest.TestCase):
    def setUp(self):
        self._knight = Knight()

    def test_next_valid_positions(self):
        expected_positions = ['a3', 'c3', 'd2']
        actual_positions = [str(p)
                            for p in self._knight.next_valid_positions()]

        for ap in actual_positions:
            self.assertTrue(ap in expected_positions)


if __name__ == '__main__':
    unittest.main()
