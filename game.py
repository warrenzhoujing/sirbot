#!/usr/bin/env python3
import logging
import requests
import random

from constants import Color
from bishop import Bishop
from king import King
from pawn import Pawn
from knight import Knight
from rook import Rook
from queen import Queen
from position import DUMMY_POSITION, Position


logging.basicConfig(level=logging.DEBUG)


class Game:
    def __init__(self, lichess, id, user_id, user_name):
        self._lichess = lichess
        self._id = id
        self._user_id = user_id
        self._user_name = user_name
        self._color = ''
        self._positions = {}

    def play(self):
        for state in self._lichess.bots.stream_game_state(self._id):
            logging.debug("Game state for '%s': %s", self._id, state)

            if self._is_my_turn(state):
                self._init_color(state)
                self._init_pieces()
                self._update_positions(state)
                self._try_move()
                self._try_promote_pawns()
            else:
                logging.debug("Not my turn: '%s'", state)
                if state['type'] == 'chatLine' and state['username'] != self._user_name:
                    self._lichess.bots.post_message(self._id, 'I cannot chat.')

    def _resign(self):
        try:
            self._lichess.bots.post_message(self._id, 'I am going to resign.')
            self._lichess.bots.resign_game(self._id)
        except requests.exceptions.HTTPError as error:
            logging.debug(error)

    def _init_color(self, state):
        self._get_color(state)

    def _init_pieces(self):
        if not self._positions:
            king = King(color=self._color)
            self._positions.update({str(king.position): king})

            queen = Queen(color=self._color)
            self._positions.update({str(queen.position): queen})

            for i in range(1, 9):
                pawn = Pawn(self._color, col=i)
                self._positions.update({str(pawn.position): pawn})

            knight = Knight(self._color, col=2)
            self._positions.update({str(knight.position): knight})

            knight = Knight(self._color, col=7)
            self._positions.update({str(knight.position): knight})

            rook = Rook(self._color, col=1)
            self._positions.update({str(rook.position): rook})

            rook = Rook(self._color, col=8)
            self._positions.update({str(rook.position): rook})

            bishop = Bishop(self._color, col=3)
            self._positions.update({str(bishop.position): bishop})

            bishop = Bishop(self._color, col=6)
            self._positions.update({str(bishop.position): bishop})

    def _take_away(self, position):
        if position in self._positions:
            gone_piece = self._positions[position]

            logging.debug("self._positions='%s'", self._positions)
            logging.debug("gone_piece='%s'", gone_piece)
            self._positions.pop(position, None)
            logging.debug("new self._positions='%s'", self._positions)

    def _update_position(self, piece, dest):
        orig = str(piece.position)
        piece.position = Position.from_string(dest)
        self._positions.update({str(piece.position): piece})
        self._positions.pop(orig, None)

    def _update_positions(self, state):
        if 'state' in state and state['type'] == 'gameFull':
            moves = state['state']['moves']
            logging.debug("moves='%s'", moves)

            all_moves = moves.split()

            for n, move in enumerate(all_moves):
                orig = move[:2]
                dest = move[2:]

                if self._is_my_move(n):
                    if orig in self._positions:
                        piece = self._positions[orig]
                        self._update_position(piece, dest)
                    else:
                        logging.error("Cannot find a piece on '%s'", orig)
                else:
                    self._take_away(dest)
        elif state['type'] == 'gameState':
            moves = state['moves']
            logging.debug("moves='%s'", moves)

            last_move = moves.split()[-1][2:]
            logging.debug("Updating last move: '%s' ...", last_move)
            self._take_away(last_move)
        else:
            logging.debug("Ignoring %s", state)

    def _get_color(self, state):
        if not self._color:
            self._color = Color.WHITE.value if state[Color.WHITE.value][
                "id"] == self._user_id else Color.BLACK.value
        return self._color

    def _is_my_move(self, number):
        return (self._color == Color.WHITE.value and number % 2 == 0) or (self._color == Color.BLACK.value and number % 2 == 1)

    def _is_my_turn(self, state):
        if state["type"] != "gameState" and state["type"] != "gameFull":
            logging.error("Unhandled state type: '%s'", state["type"])
            return False
        else:
            moves = self._get_moves(state)
            color = self._get_color(state)
            return ((len(moves) % 2 == 0) and (color == Color.WHITE.value)) or ((len(moves) % 2 == 1) and (color == Color.BLACK.value))

    def _get_moves(self, state):
        return state["moves"].split() if state["type"] == "gameState" else state["state"]["moves"].split()

    def _try_move(self, max_tries=1, current_try=1):
        logging.debug("Try moving for the %d time. %d time remaining...",
                      current_try, max_tries - current_try)

        positions = self._positions
        last_moves = list(positions.keys())
        random.shuffle(last_moves)

        for move in last_moves:
            piece = positions[move]

            next_valid_positions = piece.next_valid_positions()
            logging.debug("%s next_valid_positions=%s", str(piece),
                          [str(p) for p in next_valid_positions])

            random.shuffle(next_valid_positions)
            for position in next_valid_positions:
                try:
                    new_move = str(piece.position) + str(position)
                    logging.debug("Trying to move %s: %s", piece, new_move)
                    self._lichess.bots.make_move(self._id, new_move)

                    self._update_position(piece, str(position))

                    logging.debug("new_position=%s", str(piece))
                    return True
                except requests.exceptions.HTTPError as error:
                    logging.error("Failed to move %s to %s: '%s'",
                                  str(piece), str(position), error)

        logging.error(
            "Failed to move to a valid position for the %d time.", current_try)

        if max_tries > current_try:
            return self._try_move(current_try=(current_try + 1))
        else:
            logging.info(
                "Failed to move to a valid position for the %d time.", current_try)
            logging.info("Resigning")
            self._lichess.bots.post_message(
                self._id, 'I cannot find a good move.')
            self._resign()
            return False

    def _try_promote_pawns(self):
        logging.debug("Trying to promote pawns ...")

        logging.debug("Iterating %s ...", self._positions)
        for position, piece in self._positions.items():
            logging.debug("Checking %s ...", piece)
            logging.debug("isinstance(%s, Pawn)=%s",
                          piece, isinstance(piece, Pawn))
            logging.debug("_is_last_rank(self, %s)=%s",
                          piece.position, self._is_last_rank(piece.position))

            if isinstance(piece, Pawn) and self._is_last_rank(piece.position):
                queen = Queen(color=self._color)
                queen.position = piece.position
                self._positions.update({str(queen.position): queen})
                logging.debug("Promoting %s to %s", piece, queen)

        logging.debug("Trying to promote pawns ... done")

    def _is_last_rank(self, position):
        color = self._color
        white = Color.WHITE.value
        black = Color.BLACK.value

        row = position.row

        logging.debug("_is_last_rank: position=%s color=%s row=%d",
                      position, color, row)

        return (color == white and row == 8) or (color == black and row == 1)
