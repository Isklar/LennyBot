import aiohttp
import asyncio
import copy
import datetime
import discord
import json
import logging
import os
import re
import sys
import traceback
from collections import Counter
from discord.ext import commands

try:
    import credentials
except:
    pass


description = """
Hello! I am a bot written by Isk to provide lennyface for your amusement
"""

DISCORD_BOTS_API ='https://bots.discord.pw/api'
logChannel = int(os.environ['logChannel'])

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
log.addHandler(handler)

initial_extensions = (
    'cogs.lenny',
    'cogs.status',
)

def _prefix_callable(bot, msg):
    user_id = bot.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id}> ', 'lennyface ']
    return base

class LennyBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=_prefix_callable, description=description, pm_help=None, help_attrs=dict(hidden=True))

        self.session = aiohttp.ClientSession(loop=self.loop)
        self.client_token = os.environ['token']
        self.bots_key = os.environ.get('dbots_key', None)
        self.invite_url = os.environ['invite_url']
        self.owner_id = int(os.environ['owner'])
        self.log_channel = None
        self.currentStatus = 0

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()


    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()
        self.log_channel = discord.utils.get(self.get_all_channels(), id=logChannel)

        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.loop.create_task(self.bot_status_changer())


    async def bot_status_changer(self):
        while not self.is_closed():
            try:
                if self.currentStatus == 0:
                    game_message = '@Lenny'
                if self.currentStatus == 1:
                    game_message = 'lennyface'
                if self.currentStatus == 2:
                    game_message = 'PM for help/info'

                lenny_game = discord.Game(name=game_message, url=None, type=0)
                await self.change_presence(status=discord.Status.online, game=lenny_game)

                self.currentStatus += 1
                if self.currentStatus >= 3:
                    self.currentStatus = 0

                await asyncio.sleep(20)
            except asyncio.CancelledError as e:
                pass
            except Exception as e:
                print(e)


    async def on_resumed(self):
        print('resumed...')


    async def close(self):
        await super().close()
        await self.session.close()


    def run(self):
        super().run(self.client_token, reconnect=True)


if __name__ == '__main__':
    bot = LennyBot()
    bot.run()
    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)
