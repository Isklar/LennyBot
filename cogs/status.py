import asyncio
import aiohttp
import discord
import json
import logging

log = logging.getLogger(__name__)

DISCORD_BOTS_API = 'https://bots.discord.pw/api'

class Status:
    """Cog for updating the game."""
    def __init__(self, bot):
        self.bot = bot
        self.currentStatus = 0
        self.task = self.bot.loop.create_task(self.bot_status_changer())

    async def bot_status_changer(self):
        while not self.bot.is_closed():
            try:
                if self.currentStatus == 0:
                    game_message = '@Lenny'
                if self.currentStatus == 1:
                    game_message = 'lennyface'
                if self.currentStatus == 2:
                    game_message = 'PM for help/info'

                lenny_game = discord.Game(name=game_message, url=None, type=0)
                await self.bot.change_presence(status=discord.Status.online, game=lenny_game)

                self.currentStatus += 1
                if self.currentStatus >= 3:
                    self.currentStatus = 0

                await asyncio.sleep(20)
            except asyncio.CancelledError as e:
                pass
            except Exception as e:
                print(e)

def setup(bot):
    bot.add_cog(Status(bot))
