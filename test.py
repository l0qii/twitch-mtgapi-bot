import json
from tcg import Tcg
from mtgparser import MtgParser
from commands import Commands

# com = Commands()
# result = com.card("doubling season")
# print(result)
# result = com.price("Karn, Scion of Urza")
# print(result)

# parser = MtgParser()
# print(parser.isInSet('serum visions', 'dsadsa'))
# parse_result = json.loads(parser.parse("island unglued"))     # test card part of another card (Island in Tropical Island)
# parse_result = json.loads(parser.parse("serum visions fifth dawn"))     # test ambiguity in set name (Visions in Serum Visions)
# parse_result = json.loads(parser.parse("black lotus"))      # basic test of default set (need more variations)
# parse_result = json.loads(parser.parse("diabolic tutor"))      # synonym set is default
# parse_result = json.loads(parser.parse("black lotus"))   # another name test
# parse_result = json.loads(parser.parse("birds of paradise"))    # basic set name is default
# parse_result = json.loads(parser.parse("Karn, Scion of Urza"))  # comma in name
# parse_result = json.loads(parser.parse("gaea's cradle"))  # comma in name
# print(parse_result.get('name'))
# print(parse_result.get('set'))

tcg = Tcg()
# tcg_result = json.loads(tcg.getPrice(parse_result.get('name'), parse_result.get('set')))
tcg_result = json.loads(tcg.getPrice("city of traitors", ["exodus"]))
# tcg_result = json.loads(tcg.getPrice("city of traitors", ["exodus"]))
# tcg_result = json.loads(tcg.getPrice(parse_result.get('name'), parse_result.get('set')))
# print(str(tcg_result.get('price')))
# print(result)
# print(len(cards))
# print(card.name)