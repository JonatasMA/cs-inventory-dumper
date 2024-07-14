import time
import requests
import json
import urllib.parse

class extract_values:
    def __init__(self, steam_user):
        self.steam_url = 'https://steamcommunity.com/'
        self.steam_user = steam_user

    def get_inventory(self):
        request_url = self.steam_url + "inventory/" + self.steam_user + "/730/2?l=brazilian&count=100"
        response = requests.get(request_url)
        response = json.loads(response.content)
        return response['descriptions']

    def get_value(self, market_hash_name):
        time.sleep(5)
        market_hash_name = urllib.parse.quote_plus(market_hash_name)
        request_url = self.steam_url + "market/priceoverview/?appid=730&currency=7&market_hash_name=" + market_hash_name

        response = requests.get(request_url)
        response = json.loads(response.content)
        return response.get('lowest_price', 'R$ 0,00')

    def create_file(self):
        microtime = str(round(time.time() * 1000))
        file = open(microtime+'.csv', "w", encoding="utf8")

    def process(self, app):
        inventory = self.get_inventory()
        current_values = {}
        for iten in inventory :
            if (not 'Graffiti' in iten['market_hash_name']) and (iten['marketable'] == 1):
                # app.setLabel('current', iten['market_hash_name'])
                current_values[iten['market_hash_name']] = self.get_value(iten['market_hash_name'])
                print(iten['market_hash_name'] + ": " + current_values[iten['market_hash_name']])

        return current_values