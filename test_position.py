import unittest
from position import Position


class TestPosition(unittest.TestCase):
    def setUp(self):
        self.position = Position(5, 2)

    def test_from_string(self):
        self.assertEqual(Position.from_string('e1').col, 5)
        self.assertEqual(Position.from_string('e1').row, 1)

    def test_previous_row(self):
        self.assertEqual(self.position.previous_row(), 1)

    def test_next_row(self):
        self.assertEqual(self.position.next_row(), 3)

    def test_previous_col(self):
        self.assertEqual(self.position.previous_col(), 4)

    def test_next_col(self):
        self.assertEqual(self.position.next_col(), 6)

    def test_is_onboard_1(self):
        self.assertTrue(Position(1, 1).is_onboard())

    def test_is_onboard_2(self):
        self.assertFalse(Position(0, 1).is_onboard())

    def test_is_onboard_3(self):
        self.assertFalse(Position(9, 1).is_onboard())

    def test_is_onboard_4(self):
        self.assertFalse(Position(7, 9).is_onboard())

    def test_is_onboard_5(self):
        self.assertFalse(Position(4, 0).is_onboard())

    def test_is_onboard_6(self):
        self.assertFalse(Position(9, 0).is_onboard())

    def test_string(self):
        self.assertEqual(str(Position(5, 1)), 'e1')


if __name__ == '__main__':
    unittest.main()
