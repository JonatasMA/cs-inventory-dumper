import json
import re

class process_data:
    def __init__(self, market_json):
        self.market_history = []
        market_history = json.loads(market_json)
        self.itens_html = market_history['results_html'].split('market_listing_row market_recent_listing_row')
        self.itens_html.pop()
        for asset in market_history['assets']:
            first_asset = market_history['assets'][asset]
            key = list(first_asset.keys())[0]
            first_asset = first_asset[key]
            for iten in first_asset:
                if "appid" in first_asset[iten]:
                    if int(first_asset[iten]['appid']) == 730:
                        self.market_history.append(first_asset[iten])
        
    def fill_lists(self):
        html_itens = {}
        itens_name = {}
        for iten in self.market_history:
            html_itens[iten['market_hash_name']] = []
            itens_name[iten['name']] = iten

        return html_itens, itens_name

    def fill_values(self, html_itens, itens_name):
        regex = re.compile("""(R\$) \d+,\d+""")
        for value in self.itens_html:
            trade = re.findall('(\+)', value)
            if trade:
                price = regex.search(value)
                itens_value = price.group()
                for name in itens_name:
                    if name in value and itens_name[name]['commodity'] == 0:
                        html_itens[itens_name[name]['market_hash_name']].append(itens_value)
        
        return html_itens

    def process(self):
        html_itens, itens_name = self.fill_lists()
        
        html_itens = self.fill_values(html_itens, itens_name)

        result = {}
        for iten in html_itens:
            if len(html_itens[iten]) > 0:
                result[iten] = html_itens[iten][-0]

        return result