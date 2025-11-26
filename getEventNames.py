import wikipedia
from bs4 import BeautifulSoup
from utilities import * 
import csv
import pandas as pd
from datetime import datetime
import requests


def getEventNames():
    result = wikipedia.page("List of UFC events") 
    html = result.html()

    soup = BeautifulSoup(html, features='html.parser')
    pastEventsTable = soup.find('table', attrs={'id':'Past_events'})
    
    scheduledEventsTable = soup.find('table', attrs={'id':'Scheduled_events'})

    tableBody = pastEventsTable.find('tbody')

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


    scheduledEventsTable = soup.find('table', attrs={'id':'Scheduled_events'})
    scheduledBody = scheduledEventsTable.find('tbody')
    scheduledTableRows = scheduledEventsTable.find_all('tr')

    scheduledData = []

    for row in scheduledTableRows[1:]:  # Skip header row
        cells = row.find_all('td')
        if len(cells) >= 4:
            eventname = cells[0].text.strip()
            date = cells[1].text.strip()
            venue = cells[2].text.strip()
            eventlocation = cells[3].text.strip()
            scheduledData.append([eventname, date, venue, eventlocation])

# Sort by date (latest first)
    from datetime import datetime
    scheduledData.sort(key=lambda x: datetime.strptime(x[1], '%b %d, %Y'), reverse=True)

    print(scheduledData[0])


def getLatestEvent():
    result = wikipedia.page("List of UFC events")
    html = result.html()
    soup = BeautifulSoup(html, features='html.parser')

    scheduledEventsTable = soup.find('table', attrs={'id':'Scheduled_events'})
    scheduledTableRows = scheduledEventsTable.find_all('tr')

    scheduledData = []

    for row in scheduledTableRows[1:]:  # Skip header row
        cells = row.find_all('td')
        if len(cells) >= 4:
            eventname = cells[0].text.strip()
            date = cells[1].text.strip()
            venue = cells[2].text.strip()
            eventlocation = cells[3].text.strip()
            scheduledData.append([eventname, date, venue, eventlocation])

    scheduledData.sort(key=lambda x: datetime.strptime(x[1], '%b %d, %Y'), reverse=False)
    return scheduledData[0]

def getLatestEventName():
    result = wikipedia.page("List of UFC events")
    html = result.html()
    soup = BeautifulSoup(html, features='html.parser')

    scheduledEventsTable = soup.find('table', attrs={'id':'Scheduled_events'})
    scheduledTableRows = scheduledEventsTable.find_all('tr')

    scheduledData = []

    for row in scheduledTableRows[1:]:  # Skip header row
        cells = row.find_all('td')
        if len(cells) >= 4:
            eventname = cells[0].text.strip()
            date = cells[1].text.strip()
            venue = cells[2].text.strip()
            eventlocation = cells[3].text.strip()
            scheduledData.append([eventname, date, venue, eventlocation])

    scheduledData.sort(key=lambda x: datetime.strptime(x[1], '%b %d, %Y'), reverse=False)
    return scheduledData[0][0]

def postLatestEvent():
    latestEvent = getLatestEvent()
    
    body = {
        'eventname': latestEvent[0],
        'starttimeest': latestEvent[1], 
        'eventlocation': latestEvent[3]
    }
    
    print(body)

    response = requests.post('https://zdcdh4dtx0.execute-api.us-east-1.amazonaws.com/prd/event', json=body)
    return response




def main():
    postLatestEvent()
    # latestEventName = getLatestEventName()
    # print(latestEventName)


if __name__ == '__main__':
    main()
    