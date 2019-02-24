#!/usr/bin/env python3

import logging

from position import Position
from constants import Color

logging.basicConfig(level=logging.DEBUG)


class Pawn:
    def __init__(self, color=Color.WHITE.value, col=1):
        self._color = color
        row = 2 if self._color == Color.WHITE.value else 7
        self._position = Position(col, row)

    def __str__(self):
        return "Pawn(%s, %s)" % (self._color, self._position)

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

        1. Make a list of positions the Pawn can move no matter if it's legal or not
        2. Filter out the illegal positions

        Illegal positions:
        Outside of board (DONE)

        Returns:
        list: A list of legal positions
        """

        positions = []

        positions.extend(self._forward_positions())
        positions.extend(self._take_positions())

        return [p for p in positions if p.is_onboard()]

    def _take_positions(self):
        positions = []
        pos = self._position

        new_row = pos.row + (1 if self._color == Color.WHITE.value else -1)
        new_col = pos.col + 1
        positions.append(Position(new_col, new_row))

        new_row = pos.row + (1 if self._color == Color.WHITE.value else -1)
        new_col = pos.col - 1
        positions.append(Position(new_col, new_row))

        return positions

    def _forward_positions(self):
        positions = []
        pos = self._position

        new_row = pos.row + (2 if self._color == Color.WHITE.value else -2)
        positions.append(Position(pos.col, new_row))

        new_row = pos.row + (1 if self._color == Color.WHITE.value else -1)
        positions.append(Position(pos.col, new_row))

        return positions
