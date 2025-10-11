import wikipedia
from bs4 import BeautifulSoup
from utilities import * 
import pandas as pd


def getEventNames():
    result = wikipedia.page("List of UFC events") 
    html = result.html()

    soup = BeautifulSoup(html, features='html.parser')
    table = soup.find('table', attrs={'id':'Past_events'})
    tableBody = table.find('tbody')

    tableRows = tableBody.find_all('tr')

    data = []

    ufc12Found = False
    i = 1
    while not ufc12Found :
        row = tableRows[i]
        rowCells = row.find_all('td')
        eventName = rowCells[1].text.strip()
        data.append(eventName)
        if(eventName == 'UFC 12: Judgement Day'):
            ufc12Found = True
        i+=1
    df = pd.DataFrame(data)
    df.Name = 'EventName'
    df.to_csv('data.csv', index=False, encoding='utf-8', header=['EventName'])