import commands.woodcutting.ChopCommand as command_chop
import commands.firemaking.BurnCommand as command_burn
import commands.thieving.PickpocketCommand as command_pickpocket
import commands.stats.StatsCommand as command_stats
import commands.stats.XpCommand as command_xp
import commands.stats.LvlCommand as command_lvl

import commands.map.MoveCommand as command_move
import commands.map.LookCommand as command_look


class CommandController:
    commands = None
    auth = None
    command = None
    target = None
    author = None
    message = None
    character = None
    token = None

    def __init__(self, game):
        self.game = game
        self.commands = {
            "burn": command_burn.exec,
            "chop": command_chop.exec,
            "pickpocket": command_pickpocket.exec,
            "stats": command_stats.exec,
            "move": command_move.exec,
            "look": command_look.exec,
            "xp": command_xp.exec,
            "lvl": command_lvl.exec,
        }

    async def run(self, command, target, author, message, character, token):
        split = message.split()
        command_string = split[0][1:]

        try:
            if command_string in self.commands:
                await self.game.process_response(command, target, await self.commands[command_string](self.game, command, target, author, message, character, token))
            else:
                await self.game.process_response(command, target, "Error: command not found")
        except Exception as e:
            await self.game.process_response(command, target, "Error: {}".format(e))
