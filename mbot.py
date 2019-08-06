from twitchio.ext import commands as tcommands
from commands import Commands
import os

class Mbot(tcommands.Bot):
    """Create our IRC Twitch Bot.
    api_token is optional, but without it, you will not be able to make certain calls to the API."""

    NICK = 'onulet'

    def __init__(self):
        super().__init__(prefix='!', irc_token=os.environ['IRC_TOKEN'], api_token='API_TOKEN', client_id='CLIENT_ID',
                         nick=self.NICK, initial_channels=['kevin_spicy','rexhavoc'])
        self._commands = Commands()

    async def event_ready(self):
        """Event called when the bot is ready to go!"""
        print('READY!')

    async def event_message(self, message):
        """Event called when a message is sent to a channel you are in."""
        await self.handle_commands(message)

    @tcommands.command(name='card')
    async def card_lookup(self, ctx):
        await ctx.send(self._commands.card(ctx.content[6:]))

    @tcommands.command(name='price')
    async def card_price(self, ctx):
        await ctx.send(self._commands.price(ctx.content[6:]))

    @tcommands.command(name='shop')
    async def link_shop(self, ctx):
        await ctx.send(self._commands.link_shop())

    @tcommands.command(name='uptime')
    async def uptime(self, ctx):
        print()
        await ctx.send(self._commands.uptime(ctx.channel))

bot = Mbot()
bot.run()
