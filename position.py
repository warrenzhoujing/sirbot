import logging


class Position:
    """A valid chess board position.

    col is in the range of [1, 8]
    row is in the range of [1, 8]
    """

    @classmethod
    def from_string(cls, position):
        """Construct a Position instance with a string representation.

        Args:
            position: a string representation of a position such as 'e5'

        Returns:
            A new position object
        """
        col = int(ord(position[:1]) - ord('a')) + 1
        row = int(position[1:2])

        return cls(col, row)

    def __init__(self, col, row):
        self._col = col
        self._row = row

    def __str__(self):
        return chr(ord('a') + self._col - 1) + str(self._row)

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    def previous_row(self):
        return self._row - 1

    def next_row(self):
        return self._row + 1

    def previous_col(self):
        return self._col - 1

    def next_col(self):
        return self._col + 1

    def is_onboard(self):
        return (self._row <= 8 and self._row >= 1) and (self._col <= 8 and self._col >= 1)


DUMMY_POSITION = Position(-1, -1)
