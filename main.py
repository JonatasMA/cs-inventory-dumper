from appJar import gui
from process_data import process_data
import json

def press():
    marketHistory = app.getEntry("marketHistory")
    idUser = app.getEntry("idUser")
    file = open(marketHistory, "r", encoding="utf8")
    file = file.read()
    pd = process_data(file)
    result = pd.process()
    resultJson = open('result.json', 'x', encoding="utf8")
    resultJson.write(json.dumps(result))
    # print("abc".split('b').pop())

app = gui("CS Inventory Dumper", '500x200')
# app.addLabel("lblMarketHistory", "Market history:")
app.addLabel('guide', 'Click on link below, and save the content with Ctrl+s on your browser')
app.addWebLink('click_me', 'https://steamcommunity.com/market/myhistory?count=500')
app.addLabel('guide2', 'Input the saved file')
app.addLabelFileEntry(title="marketHistory", label="Market history:")
app.addLabelEntry(title='idUser', label="ID User:")
app.addButton('dump', press)
app.go()