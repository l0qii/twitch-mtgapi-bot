import json
import os
import re

class MtgParser:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        self._set_data = json.load(open(os.path.join(self.BASE_DIR, 'data/sets.json')))
        self._mtg_data = json.load(open(os.path.join(self.BASE_DIR, 'data/mtgfulldb.json')))
        self._card_names = [x.get('name') for x in self._mtg_data.get('cards')]

    def parse(self, text):
        result = {}
        # result = [x for x in set_data.get('sets') if (text.lower() in x.get('name').lower())
        #           or (text.lower() in x.get('synonyms').lower())]
        # print(result)

        # set_names = [x.get('name') for x in set_data.get('sets')]
        # set_abrs = [x.get('abbreviation') for x in set_data.get('sets') if x.get('abbreviation') != None]
        # synsets = [x.get('synonyms') for x in set_data.get('sets') if len(x.get('synonyms')) > 0]

        result['set'] = []
        for set in self._set_data.get('sets'):
            if set.get('name').lower() in text.lower() and len(set.get('name')) > len(result['set']):
                    result['set'].append(set.get('name'))
            if set.get('abbreviation') is not None:
                # for readability
                s = set.get('abbreviation').lower()
                # don't match an abbr if it's in the middle of another word
                if re.search('[^\w]{}[^\w]|^{}[^\w]|[^\w]{}$'.format(s, s, s), text.lower()):
                    if not set.get('name') in result['set']:
                        result['set'].append(set.get('name'))
            if len(set.get('synonyms')) > 0:
                for synonym in set.get('synonyms'):
                    if re.search('[^\w]{}[^\w]|^{}[^\w]|[^\w]{}$'.format(synonym.lower(), synonym.lower(), synonym.lower()), text.lower()) and len(synonym) > len(result['set']):
                        if not set.get('name') in result['set']:
                            result['set'].append(set.get('name'))
        # payload = "{ 'filters': [ { 'name': 'productName', 'values':  ['\"serum visions\"']  }, { 'name': 'setName', 'values':  ['"+','.join('"'+item+'"' for item in result['set'])+"']  } ]}"
        # print(payload)
        result['name'] = ""
        for card_name in self._card_names:
            if card_name.lower() in text.lower() and len(card_name) > len(result['name']):
                result['name'] = card_name

        # validate set array
        for set in result['set']:
            if not self.isInSet(result['name'], set):
                result['set'].remove(set)

        # if no set, set as default
        if len(result['set']) == 0:
            default = [x['defaultset'] for x in self._mtg_data['cards'] if x['name'] == result['name']][0]
            default = [x['name'] for x in self._set_data['sets'] if default in x['synonyms'] or x['name'] == default][0]
            result['set'].append(default)

        return json.dumps(result)

    # check if a card is in a set
    def isInSet(self, card, set):
        for c in self._mtg_data['cards']:
            if c['name'].lower() == card.lower() and set.lower() in [x.lower() for x in c['sets']]:
                return True
        return False

    # check if a card name exists
    def nameExists(self, text):
        if text.lower() in [x.lower() for x in self._card_names]:
            return True
        else:
            return False

    # def __ngrams(self, input, n):
    #     input = input.split(' ')
    #     output = []
    #     for i in range(len(input) - n + 1):
    #         output.append(input[i:i + n])
    #     return output
    #
    # def __matchWord(self, inputText, toFindText):
    #     print(set(inputText) & set(toFindText))
    #     return set(inputText) & set([x.lower() for x in toFindText])