#!/usr/bin/env python3

import logging

from position import Position
from constants import Color

logging.basicConfig(level=logging.DEBUG)


class Rook:
    def __init__(self, color=Color.WHITE.value, col=1):
        if col != 1 and col != 8:
            raise AssertionError
        self._color = color
        row = 1 if self._color == Color.WHITE.value else 8
        self._position = Position(col, row)

    def __str__(self):
        return "Rook(%s, %s)" % (self._color, self._position)

    def __repr__(self):
        return self.__str__()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    def next_valid_positions(self):
        """Calculate the next valid positions based on the current position.

        1. Make a list of positions the Knight can move no matter if it's legal or not
        2. Filter out the illegal positions

        Illegal positions:
        Outside of board (DONE)

        Returns:
        list: A list of legal positions
        """

        positions = []

        row = self._position.row
        col = self._position.col

        for i in range(1, 8):
            positions.append(Position(row=row + i, col=col))
            positions.append(Position(row=row - i, col=col))
            positions.append(Position(row=row, col=col + i))
            positions.append(Position(row=row, col=col - i))

        return [p for p in positions if p.is_onboard()]
