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
        self._parser = MtgParser()

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
        cardname = ctx.content[6:]
        if self._parser.nameExists(cardname):
            cardname = '"' + cardname + '"'
        cards = Card.where(name=cardname).all()
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
        parse_result = json.loads(self._parser.parse(ctx.content[6:]))
        tcg = Tcg()
        try:
            tcg_result = json.loads(tcg.getPrice(parse_result.get('name'), parse_result.get('set')))
            if 'error' in tcg_result:
                response = tcg_result.get('error')
            if tcg_result:
                response = '{} from {} is currently selling at ${}'.format(parse_result.get('name'), parse_result.get('set'), tcg_result.get('price'))
        except ValueError as e:
            response = e
        await ctx.send(response)

bot = Mbot()
bot.run()


# parser = MtgParser()
# parse_result = json.loads(parser.parse("unlimited black lotus"))
# tcg = Tcg()
# tcg_result = json.loads(tcg.getPrice("city of traitors", "exodus"))
# print(str(tcg_result.get('price')))
# result = json.loads(parser.parse("gaea's cradle urza's saga"))
# print(result)

# cards = Card.where(name='"ow"').all()
# card = cards[0]
# print(card.name)