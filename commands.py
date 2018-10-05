import json
from mtgsdk import Card
from tcg import Tcg
from mtgparser import MtgParser

class Commands:

    def __init__(self):
        self._parser = MtgParser()

    def card(self, inputString):
        response = 'card not found {}'.format(inputString)
        cardname = inputString
        if self._parser.nameExists(cardname):
            cardname = '"' + cardname + '"'
        cards = Card.where(name=cardname).all()
        if cards:

            # put together a nice list of some sets
            cardsets = [card.set for card in sorted(cards, key=lambda x: x.set)]
            if len(cardsets) > 6:
                cardsettext = '[' + ','.join(cardsets[:6]) + '... +' + str((len(cardsets) - 6)) + ' more]'
            else:
                cardsettext = '[' + ','.join(cardsets) + ']'

            card = cards[0]
            if 'creature' in card.type.lower():
                response = '\\\\{}// {} {}/{}, {} -- {} {}'.format(card.name, card.type, card.power, card.toughness, card.mana_cost, card.text, cardsettext)
            elif 'planeswalker' in card.type.lower():
                response = '\\\\{}// {} (Loyalty: {}), {} -- {} {}'.format(card.name, card.type, card.loyalty, card.mana_cost, card.text, cardsettext)
            elif hasattr(card, 'mana_cost'):
                response = '\\\\{}// {}, {} -- {} {}'.format(card.name, card.type, card.mana_cost, card.text,                                                             cardsettext)
            else:
                # it's a land
                response = '\\\\{}// {} -- {} {}'.format(card.name, card.type, card.text, cardsettext)
        return response

    def price(self, inputString):
        response = 'card not found {}'.format(inputString)
        parse_result = json.loads(self._parser.parse(inputString))
        tcg = Tcg()
        try:
            tcg_result = json.loads(tcg.getPrice(parse_result.get('name'), parse_result.get('set')))
            if 'error' in tcg_result:
                response = tcg_result.get('error')
            if tcg_result:
                response = '{} from {} is currently selling at ${}'.format(parse_result.get('name'),
                                                                           parse_result.get('set')[0],
                                                                           tcg_result.get('price'))
        except ValueError as e:
            response = e
        return response