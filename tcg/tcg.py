import os
import json
import requests
from tcg.config import __endpoint__

class Tcg:
    CATEGORYID = 1  # 1 is the Id for Mtg
    NOT_FOUND_ERR = "That doesn't look like a valid card to me, are you sure you spelled it right?"
    MISSING_ERR = "Hey I'm pretty smart, but I'm having trouble understanding what you're looking for"

    def getPrice(self, card, set):
        print(card)
        print(set)
        result = {}
        json_data = self.__priceLookup(self.__getProductDetails(self.__getCategoryProducts(card, set)))
        if 'success' in json_data:
            if json_data['success'] == True:
                # print(json_data)
                result['price'] = format(float(json_data['results'][0]['price']), '.2f')
                return json.dumps(result)
            else:
                raise ValueError(json_data.get('errors')[0])
        else:
            print(json_data)
            raise ValueError(self.MISSING_ERR)

    def __priceLookup(self, productConditionId):
        url = "http://api.tcgplayer.com/pricing/marketprices/{}".format(str(productConditionId))
        # url = "http://api.tcgplayer.com/pricing/marketprices/21803"
        headers = self.__getHeaders()
        response = requests.get(url, headers=headers)
        return response.json()

    # def getSearchManifest(self):
    #     url = "{}/catalog/categories/{}/search/manifest".format(__endpoint__, self.CATEGORYID)
    #     headers = self.__getHeaders()
    #     response = requests.get(url, headers=headers)
    #     return response.json()

    def __getCategoryProducts(self, _card, _set):
        card = "{}".format(_card).replace("'", "\\'")
        set = "{}".format(','.join(item for item in _set)).replace("'", "\\'")
        payload = "{ 'filters': [ { 'name': 'productName', 'values':  ['"+card+"']  }, { 'name': 'setName', 'values':  ['"+set+"']  } ]}"
        url = "{}/catalog/categories/{}/search".format(__endpoint__, self.CATEGORYID)
        headers = self.__getHeaders()
        response = requests.post(url, headers=headers, data=payload)
        json_data = response.json()
        print(json_data)
        if json_data['totalItems'] > 0:
            json_data = response.json()['results']
            return ','.join(str(x) for x in json_data)
        else:
            raise ValueError(self.NOT_FOUND_ERR)

    # API has changed to http://api.tcgplayer.com/catalog/products/{productID}/skus
    # and only 1 productId can be used at a time. This is balls, and will need to be fixed later
    def __getProductDetails(self, productIds):
        url = "{}/v1.14.0/catalog/products/{}".format(__endpoint__, productIds)
        headers = self.__getHeaders()
        response = requests.get(url, headers=headers)
        json_data = response.json()
        output_dict = [x.get('productConditions')[0].get('productConditionId') for x in json_data.get('results') if x.get('productConditions')[0].get('name') == 'Near Mint']
        return ','.join(str(x) for x in output_dict)

    def __getHeaders(self):
        return {
            "Accept" : "application/json",
            "Authorization" : os.environ['TCG_BEARER_TOKEN'],
            "Content-Type" : "application/json",
            "User-Agent": "Mozilla/5.0"
        }
