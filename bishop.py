#!/usr/bin/env python3

import logging

from position import Position
from constants import Color

logging.basicConfig(level=logging.DEBUG)


class Bishop:
    def __init__(self, color=Color.WHITE.value, col=3):
        if col != 3 and col != 6:
            raise AssertionError
        self._color = color
        row = 1 if self._color == Color.WHITE.value else 8
        self._position = Position(col, row)

    def __str__(self):
        return "Bishop(%s, %s)" % (self._color, self._position)

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

        1. Make a list of positions the Bishop can move no matter if it's legal or not
        2. Filter out the illegal positions

        Illegal positions:
        Outside of board (DONE)

        Returns:
        list: A list of legal positions
        """

        positions = []

        row = self._position.row
        col = self._position.col

        for x in range(8):
            positions.append(
                Position(col=self._position.col + x, row=self._position.row + x))
            positions.append(
                Position(col=self._position.col + x, row=self._position.row - x))
            positions.append(
                Position(col=self._position.col - x, row=self._position.row + x))
            positions.append(
                Position(col=self._position.col - x, row=self._position.row - x))

        return [p for p in positions if p.is_onboard()]
