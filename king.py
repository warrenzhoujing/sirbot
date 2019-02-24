#!/usr/bin/env python3

import logging

from position import Position
from constants import Color

logging.basicConfig(level=logging.DEBUG)


class King:
    def __init__(self, color=Color.WHITE.value):
        self._color = color
        self._position = Position.from_string(
            'e1') if self._color == Color.WHITE.value else Position.from_string('e8')

    def __str__(self):
        return "King(%s, %s)" % (self._color, self._position)

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

        1. Make a list of positions the King can move no matter if it's legal or not
        2. Filter out the illegal positions

        Illegal positions:
        Outside of board (DONE)

        Returns:
        list: A list of legal positions
        """

        positions = []
        pos = self._position
        for r in range(pos.previous_row(), pos.next_row() + 1):
            for c in range(pos.previous_col(), pos.next_col() + 1):
                positions.append(Position(c, r))

        return [p for p in positions if p.is_onboard()]
