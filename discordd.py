import logging
import discord
import asyncio
from asyncio import coroutines
import concurrent.futures
from asyncio import futures

from discord import channel

logging.basicConfig(level=logging.INFO)

thread_lock = None

config = None
intents = discord.Intents.default()
client = discord.Client(intents=intents)
server = None
channels = {}
game = None
auth = None


class Discord:
    def __init__(self, conf, g, a):
        global config
        global thread_lock
        global channels
        global game
        global auth

        channels = conf['CHANNELS']

        config = conf
        game = g
        game.set_discord_privmsg(self.privmsg)
        auth = a

    def set_thread_lock(self, lock):
        global thread_lock
        thread_lock = lock

    def privmsg(self, target, message):
        global client
        asyncio.run_coroutine_threadsafe(
            async_privmsg(target, message), client.loop)

    def run(self):
        global config
        global client
        global game

        client.run(config["DISCORD_TOKEN"])

    def close(self):
        global client
        asyncio.run_coroutine_threadsafe(client.close(), client.loop)


async def async_privmsg(target, message):
    global client

    channel = client.get_channel(target)

    await channel.send(message.strip())


@client.event
async def on_message(message):
    global config
    global client
    global channels
    global thread_lock
    global game
    global auth

    # Don't reply to itself
    if message.author == client.user:
        return

    # with thread_lock:
    content = message.clean_content
    if len(message.attachments) > 0:
        content += ' ' + message.attachments[0].url

    if content.startswith('+') or content.startswith('-') or content.startswith('!') or content.startswith('@') or content.startswith('.'):
        nick = '{}'.format(message.author)
        if "{}".format(message.channel) == "Direct Message with {}".format(nick):
            split = content.split()
            if split[0][1:] == "login":
                if len(split) != 3:
                    await message.channel.send("Syntax: {} <username> <password>".format(split[0]))
                    return
                if auth.login(nick, split[1], split[2]):
                    await message.channel.send("Login successful!")
                else:
                    await message.channel.send("Login failed!")
            elif split[0][1:] == "register":
                if len(split) != 3:
                    await message.channel.send("Syntax: {} <username> <password>".format(split[0]))
                    return
                if auth.check(nick):
                    await message.channel.send("You are already logged in.")
                elif auth.register(split[1], split[2]):
                    await message.channel.send("Registration successful! Now you may log in.")
                else:
                    await message.channel.send("Registration failed! Common failures: username already exists, password too short.")
            elif content[1:] == "logout":
                if auth.check(nick):
                    auth.logout(nick)
                    await message.channel.send("Logout successful!")
                else:
                    await message.channel.send("You are not logged in.")
            elif content[1:] == "loggedin":
                if auth.check(nick):
                    await message.channel.send("Successfully logged in!")
                else:
                    await message.channel.send("Not currently logged in.")
            elif content[1:] == "help":
                await message.author.send("{}/help".format(config['HOSTNAME']))
        elif message.channel.id in channels:
            if content[1:] == "help":
                await message.author.send("{}/help".format(config['HOSTNAME']))
                return
            elif not auth.check(nick):
                await message.author.send("You are not logged in.")
                return
            print('[Discord] [#{}] CMD DETECTED: ({}) {}'.format(
                message.channel, nick, content))
            await game.command(auth, message.channel.send, None, message.author, content)
