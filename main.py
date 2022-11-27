#!/usr/bin/env python3

import asyncio
import json
import os
import signal
import sys
import threading

from auth import *
from discordd import *
from game import *
from dotenv import load_dotenv

print("Loading SwiftRPG...")

load_dotenv()

config = {
    'DISCORD_TOKEN': os.getenv('DISCORD_TOKEN'),
    'CHANNELS': json.loads(os.getenv('CHANNELS')),
    'HOSTNAME': os.getenv('HOSTNAME'),
    'OWNER': os.getenv('OWNER'),
}


def discord(argv, game, auth):
    print("Connecting to Discord... ({})".format(argv))

    discord_process = Discord(config, game, auth)

    discord_process.run()


def input_thread():
    input_thread = threading.Thread(target=accept_input)
    input_thread.daemon = True
    input_thread.start()

    return input_thread


def accept_input():

    print("Accepting input...")
    while True:
        cmd = input("$ ")

        # TODO: Add commands
        if cmd == "exit":
            exit(0)


def game_thread():
    game = Game(config)
    gaming_thread = threading.Thread(target=game.start)
    gaming_thread.daemon = True
    gaming_thread.start()
    return gaming_thread, game


def main(argv):
    auth = Auth()
    gaming_thread, game = game_thread()

    discord(argv, game, auth)


def handler(signum, frame):
    exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)

    args = sys.argv[1:]
    print("Launching main() with args: {}".format(args))
    main(args)
