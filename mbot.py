from twitchio import commands as tcommands
import os
import json
import requests
from mtgsdk import Card
# from mtgsdk import Set
# from mtgsdk import Type
# from mtgsdk import Supertype
# from mtgsdk import Subtype
# from mtgsdk import Changelog
from tcg import Tcg
from mtgparser import MtgParser

class Mbot(tcommands.TwitchBot):
    """Create our IRC Twitch Bot.
    api_token is optional, but without it, you will not be able to make certain calls to the API."""

    def __init__(self):
        super().__init__(prefix=['!', '?'], token=os.environ['IRC_TOKEN'], api_token='API_TOKEN', client_id='CLIENT_ID',
                         nick='onulet', initial_channels=['#kevin_spicy'])

    async def event_ready(self):
        """Event called when the bot is ready to go!"""
        print('READY!')

    # async def event_message(self, message):
    #     """Event called when a message is sent to a channel you are in."""
    #     if message.content == 'Hello':
    #         await message.send('World!')

    @tcommands.twitch_command(aliases=['card'])
    async def card_lookup(self, ctx):
        response = 'card not found {}'.format(ctx.content[6:])
        cards = Card.where(name=ctx.content[6:]).all()
        if cards:
            card = cards[0]
            if 'creature' in card.type.lower():
                response = '\\\\{}// {} {}/{}, {} -- {}'.format(card.name, card.type, card.power, card.toughness, card.mana_cost, card.text)
            elif 'planeswalker' in card.type.lower():
                response = '\\\\{}// {} (Loyalty: {}), {} -- {}'.format(card.name, card.type, card.loyalty, card.mana_cost, card.text)
            else:
                response = '\\\\{}// {}, {} -- {}'.format(card.name, card.type, card.mana_cost, card.text)
        await ctx.send(response)

    @tcommands.twitch_command(aliases=['price'])
    async def card_price(self, ctx):
        response = 'card not found {}'.format(ctx.content[6:])
        parser = MtgParser()
        parse_result = json.loads(parser.test(ctx.content[6:]))
        tcg = Tcg()
        tcg_result = tcg.getPrice(parse_result.get('name'), parse_result.get('set'))
        if tcg_result:
            response = '{} from {} is currently selling at ${}'.format(parse_result.get('name'), parse_result.get('set'), tcg_result)
        await ctx.send(response)

bot = Mbot()
bot.run()

# parser = MtgParser()
# result = json.loads(parser.test("unlimited black lotus"))
# print(result)
# result = json.loads(parser.test("gaea's cradle urza's saga"))
# print(result)

