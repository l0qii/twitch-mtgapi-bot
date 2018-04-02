import json
import os

class MtgParser:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        self._set_data = json.load(open(os.path.join(self.BASE_DIR, 'data/sets.json')))
        self._card_data = json.load(open(os.path.join(self.BASE_DIR, 'data/mtg_card_names.json')))
        self._card_names = [x.get('name') for x in self._card_data.get('cards')]


    def parse(self, text):
        result = {}
        # result = [x for x in set_data.get('sets') if (text.lower() in x.get('name').lower())
        #           or (text.lower() in x.get('synonyms').lower())]
        # print(result)

        # set_names = [x.get('name') for x in set_data.get('sets')]
        # set_abrs = [x.get('abbreviation') for x in set_data.get('sets') if x.get('abbreviation') != None]
        # synsets = [x.get('synonyms') for x in set_data.get('sets') if len(x.get('synonyms')) > 0]

        result['set'] = ""
        for set in self._set_data.get('sets'):
            if set.get('name').lower() in text.lower() and len(set.get('name')) > len(result['set']):
                result['set'] = set.get('name')
            if set.get('abbreviation') is not None:
                if set.get('abbreviation').lower() in text.lower():
                    result['set'] = set.get('name')
            if len(set.get('synonyms')) > 0:
                for synonym in set.get('synonyms'):
                    if synonym.lower() in text.lower() and len(synonym) > len(result['set']):
                        result['set'] = set.get('name')

        result['name'] = ""
        for card_name in self._card_names:
            if card_name.lower() in text.lower() and len(card_name) > len(result['name']):
                result['name'] = card_name
        return json.dumps(result)

    def nameExists(self, text):
        if text.lower() in [x.lower() for x in self._card_names]:
            return True
        else:
            return False

    def __ngrams(self, input, n):
        input = input.split(' ')
        output = []
        for i in range(len(input) - n + 1):
            output.append(input[i:i + n])
        return output

    def __matchWord(self, inputText, toFindText):
        print(set(inputText) & set(toFindText))
        return set(inputText) & set([x.lower() for x in toFindText])