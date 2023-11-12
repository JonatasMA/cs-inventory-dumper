import time
import requests

class extract_values:
    def __init__(self, steam_user):
        self.steam_url = 'https://steamcommunity.com/'
        self.steam_user = steam_user

    def get_inventory(self):
        request_url = self.steam_url + "inventory/76561198286681262/730/2?l=brazilian&count=75"

        return requests.get(url);

    def create_file(self):
        microtime = str(round(time.time() * 1000))
        file = open(microtime+'.csv', "w", encoding="utf8")