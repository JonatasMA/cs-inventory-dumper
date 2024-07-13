from appJar import gui
from process_data import process_data
from extract_values import extract_values
import json
import csv

def press():
    marketHistory = app.getEntry("marketHistory")
    idUser = app.getEntry("idUser")
    file = open(marketHistory, "r", encoding="utf8")
    file = file.read()
    pd = process_data(file).process()
    vd = extract_values(idUser).process(app)

    with open('result.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        spamwriter.writerow(['Item', 'Valor Pago', 'Valor Atual', 'Diferença'])
        index = 2
        for key, value in vd:
            spamwriter.writerow([key, pd[key], value, "=((C{index}-B{index})/B{index})"])
            index = index + 1

        spamwriter.writerow([])
        spamwriter.writerow(['Total', '=SUM(B2:B39)', '=(SUM(C2:C39))', '=((C41-B41)/B41)'])

app = gui("CS Inventory Dumper", '500x200')
# app.addLabel("lblMarketHistory", "Market history:")
app.addLabel('guide', 'Click on link below, and save the content with Ctrl+s on your browser')
app.addWebLink('click_me', 'https://steamcommunity.com/market/myhistory?count=500')
app.addLabel('guide2', 'Input the saved file')
app.addLabelFileEntry(title="marketHistory", label="Market history:")
app.addLabelEntry(title='idUser', label="ID User:")
app.addButton('dump', press)
app.addLabel('current', '')
app.go()