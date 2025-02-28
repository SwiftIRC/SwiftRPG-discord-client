#!/usr/bin/env python3

from types import FunctionType
import API.api as api
import os
import time
import controllers.CommandController as CommandController

from auth import *


class Game:
    ssl_verify = True
    discord_privmsg = None
    config = {}

    def __init__(self, config):
        if os.getenv('SSL_VERIFY'):
            self.ssl_verify = bool(int(os.getenv('SSL_VERIFY')))
        self.config = config
        self.game_controller = CommandController.CommandController(self)

    def set_discord_privmsg(self, discord_privmsg):
        self.discord_privmsg = discord_privmsg

    def start(self):
        while True:
            time.sleep(300)

    async def xp(self, level: int):
        return level + 10 * level ** 3

    async def level(self, xp: int):
        for i in range(0, 101):
            if await self.xp(i) > xp:
                return i-1
        return 100

    async def process_response(self, command, target, response):
        if response != None and len(response) > 0:
            await command(content=response)

    async def process_private_response(self, command, target, response):
        await target.send(response)

    async def command(self, auth: Auth, command: FunctionType, target: FunctionType, author: string, message: string):
        character = await auth.get_character(str(author))
        token = await auth.get_token(str(author))
        response = await self.game_controller.run(command, target, author, message, character, token)
        await self.process_response(command, target, response)

    #     split = message.split()
    #     if message[1:] == 'foo':
    #         await self.process_response(command, target, "What's up, {}?".format(author))
    #     elif message[1:] == 'help':
    #         await self.process_private_response(command, author, "{}/help".format(os.getenv('HOSTNAME')))
    #     elif split[0][1:] == 'xp' or split[0][1:] == 'exp':
    #         if len(split) != 2:
    #             await self.process_response(command, target, "Usage: {} <level>".format(split[0]))
    #             return
    #         xp = await self.xp(int(split[1]))
    #         await self.process_response(command, target, "Level {} is equivalent to {} XP".format(split[1], xp))
    #     elif split[0][1:] == 'level' or split[0][1:] == 'lvl':
    #         if len(split) != 2:
    #             await self.process_response(command, target, "Usage: {} <experience>".format(split[0]))
    #             return
    #         level = await self.level(int(split[1]))
    #         await self.process_response(command, target, "XP of {} is equivalent to level {}".format(split[1], level))
    #     elif split[0][1:] == 'stats':
    #         if len(split) != 2:
    #             response = await api.get(command, target, token, 'stats')
    #         else:
    #             character = split[1]
    #             response = await api.get(command, target, token, 'stats/{}'.format(split[1]))
    #         print(response)
    #         await self.process_response(command, target, "Stats: {} - Thieving: {} - Woodcutting: {}".format(character, response['thieving'], response['woodcutting']))
    #     # Thieving
    #     elif message[1:] == 'pickpocket':
    #         response = await api.post(
    #             self, command, target, token, 'thieving/pickpocket')
    #         if response:
    #             await self.process_response(command, target, "[{}] 🕵️ Thieving: {} ({}xp) - Gold: {}".format(character, await self.level(response.get('thieving', 0)), response.get('thieving', 0), response.get('gold', 0)))
    #     elif message[1:] == 'steal':
    #         response = await api.post(
    #             self, command, target, token, 'thieving/steal')
    #         if response:
    #             await self.process_response(command, target, "[{}] 🕵️ Thieving: {} ({}xp) - Gold: {}".format(character, await self.level(response.get('thieving', 0)), response.get('thieving', 0), response.get('gold', 0)))
    #     elif message[1:] == 'pilfer':
    #         response = await api.post(
    #             self, command, target, token, 'thieving/pilfer')
    #         if response:
    #             await self.process_response(command, target, "[{}] 🕵️ Thieving: {} ({}xp) - Gold: {}".format(character, await self.level(response.get('thieving', 0)), response.get('thieving', 0), response.get('gold', 0)))
    #     elif message[1:] == 'plunder':
    #         response = await api.post(
    #             self, command, target, token, 'thieving/plunder')
    #         if response:
    #             await self.process_response(command, target, "[{}] 🕵️ Thieving: {} ({}xp) - Gold: {}".format(character, await self.level(response.get('thieving', 0)), response.get('thieving', 0), response.get('gold', 0)))
    #         pass
    #     # Fishing
    #     elif message[1:] == "net":
    #         pass
    #     elif message[1:] == "lure":
    #         pass
    #     elif message[1:] == "angle":
    #         pass
    #     # Woodcutting
    #     elif message[1:] == "chop":
    #         response = await api.post(
    #             self, command, target, token, 'woodcutting/chop')
    #         if response:
    #             await self.process_response(command, target, "[{}] 🪓 Woodcutting: {} ({}xp) - Logs: {}".format(character, await self.level(response.get('woodcutting', 0)), response.get('woodcutting', 0), response.get('logs', 0)))
    #         pass
    #     # Mining
    #     elif message[1:] == "mine":
    #         pass
    #     # Smithing
    #     elif message[1:] == "smith":
    #         pass
    #     # Crafting
    #     elif message[1:] == "craft":
    #         pass
    #     # Cooking
    #     elif message[1:] == "cook":
    #         pass
