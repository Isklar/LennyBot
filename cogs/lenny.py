import asyncio
import aiohttp
import discord
import json
import logging

log = logging.getLogger(__name__)

DISCORD_BOTS_API = 'https://bots.discord.pw/api'

class Lenny:
    """Cog for responding with the lennyface and (if permitted), deleting the invoking message."""
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.author != self.bot.user and not message.author.bot:
            channel = message.channel
            if message.author.id == self.bot.owner_id:
                if 'servers' in message.content.lower():
                    numServers = len(self.bot.guilds)
                    numUsers = sum(1 for i in self.bot.get_all_members())
                    await self.bot.log_channel.send('{} servers, {} users.'.format(str(numServers), str(numUsers)))

            if type(channel) != discord.channel.TextChannel:
                await self.log(message)

                if 'lennyface' in message.content.lower() or self.bot.user.mentioned_in(message) and not message.mention_everyone:
                    await channel.send('( ͡° ͜ʖ ͡°)')

                else:
                    async with channel.typing():
                        embed = discord.Embed(title = "Invite Lenny:", color = 0xD1526A)
                        embed.description = "[Click me!]({})".format(self.bot.invite_url)
                        avatar = self.bot.user.avatar_url or self.bot.user.default_avatar_url
                        embed.set_author(name = "Lenny (Discord ID: {})".format(self.bot.user.id), icon_url = avatar)
                        embed.add_field(name = "Triggers: ", value = "`lennyface`\n{}".format(self.bot.user.mention))
                        me = discord.utils.get(self.bot.get_all_members(), id=self.bot.owner_id)
                        avatar = me.default_avatar_url if not me.avatar else me.avatar_url
                        embed.set_footer(text = "Developer/Owner: {0} (Discord ID: {0.id}) - Shard ID: {1}".format(me, self.shard_id), icon_url = avatar)
                        await channel.send('', embed = embed)
                        await channel.send('Support server: https://discord.gg/nwYjRz4')

            ## Lennyface send / delete
            if 'lennyface' in message.content.lower() or self.bot.user.mentioned_in(message) and not message.mention_everyone:
                if type(channel) == discord.channel.TextChannel:
                    await channel.send('( ͡° ͜ʖ ͡°)')
                    await self.log(message)

                if (message.content.lower() == 'lennyface') or (message.content.lower() == self.bot.user.mention):
                    try:
                        await message.delete()
                    except discord.errors.Forbidden as e:
                        pass
                    except Exception as e:
                        log.info(e)

            elif 'lenny' in message.content.lower():
                if type(channel) == discord.channel.TextChannel:
                    await self.log(message)
                else:
                    await self.log(message)


    async def log(self, message):
        """
        This will be the main function to log things to the `logChannel`
        Hopefully this will make it so things don't get different formats, it will all be the same.
        """
        if self.bot.log_channel is None:
            return
        try:
            if type(message.channel) == discord.channel.TextChannel:
                await self.bot.log_channel.send('[{0.author.guild.name}] {0.author.name} - {0.clean_content}'.format(message))
            else:
                await self.bot.log_channel.send(':mailbox_with_mail: {0.author.name} - {0.clean_content}'.format(message))
        except Exception as e:
            print("Failed to log\n{}".format(e))

def setup(bot):
    bot.add_cog(Lenny(bot))
