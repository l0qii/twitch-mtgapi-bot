import os
import requests
from tcg.config import __endpoint__

class Tcg:
    CATEGORYID = 1  # 1 is the Id for Mtg
    NOT_FOUND_ERR = "Card not found"

    # def getProductConditionId(self, card):
    #     payload = {'categoryId': '1', 'productName': card}
    #     url = "http://api.tcgplayer.com/catalog/products"
    #     headers = self.__getHeaders()
    #     response = requests.get(url, headers=headers, params=payload)
    #     data = response.json()
    #     productConditionId = data['results'][0]['productConditions'][0]['productConditionId']
    #     print(self.getPrice(productConditionId))
    #
    # def getGroupId(self, set):
    #     payload = {'categoryId': '1', 'name': set}
    #     url = "http://api.tcgplayer.com/catalog/groups"
    #     headers = self.__getHeaders()
    #     response = requests.get(url, headers=headers, params=payload)
    #     data = response.json()
    #     # print(data)
    #     # productConditionId = data['results'][0]['productConditions'][0]['productConditionId']
    #     print(data)

    def getPrice(self, card, set):
        json_data = self.__priceLookup(self.__getProductDetails(self.__getCategoryProducts(card, set)))
        if json_data['success'] == True:
            return format(float(json_data['results'][0]['price']), '.2f')
        else:
            raise ValueError(json_data.get('errors')[0])

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
        set = "{}".format(_set).replace("'", "\\'")
        payload = "{ 'filters': [ { 'name': 'productName', 'values':  ['"+card+"']  }, { 'name': 'setName', 'values':  ['"+set+"']  } ]}"
        # payload = {'productName': card, 'setName': set}
        url = "{}/catalog/categories/{}/search".format(__endpoint__, self.CATEGORYID)
        headers = self.__getHeaders()
        response = requests.post(url, headers=headers, data=payload)
        json_data = response.json()
        print(payload)
        if json_data['totalItems'] > 0:
            json_data = response.json()['results']
            return ','.join(str(x) for x in json_data)
        else:
            raise ValueError(self.NOT_FOUND_ERR)

    def __getProductDetails(self, productIds):
        url = "{}/catalog/products/{}".format(__endpoint__, productIds)
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
