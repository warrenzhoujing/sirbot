#!/usr/bin/env python3

from enum import Enum


class NoValue(Enum):
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)


class Event(NoValue):
    CHALLENGE = "challenge"
    GAME = "game"


class Color(NoValue):
    WHITE = "white"
    BLACK = "black"
