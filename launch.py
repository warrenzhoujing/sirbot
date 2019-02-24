#!/usr/bin/env python3

from argparse import ArgumentParser
import logging
import requests

import berserk

from constants import Event
from game import Game


logging.basicConfig(level=logging.DEBUG)

games = {}


def getGame(lichess, challenge_id, user_id, user_name):
    if challenge_id not in games:
        game = Game(lichess, challenge_id, user_id, user_name)
        games[challenge_id] = game
    return games[challenge_id]


def config_argparser():
    parser = ArgumentParser(description='Play a lichess game as a BOT')

    parser.add_argument("token_file")

    return parser.parse_args()


def main():
    args = config_argparser()
    logging.debug("Using token: %s", args.token_file)

    user_name = args.token_file.split('.')[0]
    user_id = user_name.lower()
    logging.debug("user_id=%s", user_id)

    with open(args.token_file, 'r') as id_file:
        token = id_file.read().strip()
    logging.debug("token=%s", token)

    lichess = berserk.Client(berserk.TokenSession(token))

    for event in lichess.bots.stream_incoming_events():
        logging.debug("Incoming event for '%s': %s", user_id, event)

        if event["type"] == Event.CHALLENGE.value:
            challenge = event[Event.CHALLENGE.value]
            challenge_id = challenge["id"]
            challenger_id = challenge["challenger"]["id"]
            if not challenge["rated"]:
                lichess.bots.accept_challenge(challenge_id)
                logging.info("Casual challenge '%s' accepted from '%s'",
                             challenge_id, challenger_id)

                game = getGame(lichess, challenge_id, user_id, user_name)
                logging.debug("game=%s", game)
                game.play()
            else:
                lichess.bots.decline_challenge(challenge_id)
                logging.info("Rated challenge '%s' declined from '%s'",
                             challenge_id, challenger_id)
        else:
            challenge_id = event[Event.GAME.value]["id"]
            logging.info("Trying to play existing game: '%s'", challenge_id)
            game = getGame(lichess, challenge_id, user_id, user_name)
            game.play()


if __name__ == "__main__":
    main()
