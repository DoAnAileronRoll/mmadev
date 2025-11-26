import wikipedia
from bs4 import BeautifulSoup
from utilities import *
from getEventNames import getEventNames
import requests
from getEventNames import getLatestEventName


def getCardInfo(eventname):
    result = wikipedia.page(eventname)
    html = result.html()

    soup = BeautifulSoup(html, features='html.parser')
    table = soup.find(
        'table', attrs={'class': 'toccolours', 'style': 'font-size: 85%;'})
    tableBody = table.find('tbody')

    cardSections = []
    curCardSectionIndex = 0
    cardsectiontitle = ""
    for index, row in enumerate(tableBody.find_all('tr')):
        allHeadersInRow = row.find_all('th')
        if (len(allHeadersInRow) == 1):
            cardsectiontitle = allHeadersInRow[0].text.strip()
            cardSections.append({
                'title': cardsectiontitle,
                'fights': []
            })
            curCardSectionIndex = len(cardSections) - 1
        elif (len(allHeadersInRow) == 0):
            vals = row.find_all('td')

            weightclass = vals[0].text.strip()
            fighter1name = vals[1].text.strip()
            winnerindicator = vals[2].text.strip()  # either def. or vs.
            fighter2name = vals[3].text.strip()
            method = vals[4].text.strip()
            round = vals[5].text.strip()
            time = vals[6].text.strip()
            notes = vals[7].text.strip()

            weightInfo = parseWeight(weightclass)
            istitlefight = 1 if '(c)' in fighter1name or '(c)' in fighter2name else 0

            cardsection = ""
            if (cardsectiontitle.find("Early") != -1):
                cardsection = "Early Prelims"
            elif (cardsectiontitle.find("Prelim") != -1):
                cardsection = "Prelims"
            else:
                cardsection = "Main Card"

            if method == "":
                body = {
                    "cardsection": cardsection,
                    'weightclass': weightInfo[0],
                    'catchweightlimit': weightInfo[1],
                    'fighter1name': fighter1name,
                    'fighter2name': fighter2name,
                    'istitlefight': istitlefight,
                    'eventname': eventname
                }
                cardSections[curCardSectionIndex]['fights'].append(body)
            else:
                judgescore1 = isdraw = isnocontest = judgescore2 = judgescore3 = losername = winnername = None

                methodText = vals[4].text.strip()
                if (winnerindicator == 'def.'):
                    winnername = fighter1name
                    losername = fighter2name
                    isdraw = 0
                    isnocontest = 0

                if (methodText.find('Decision') > -1 or methodText.find('Draw') > -1):
                    parsedDecisionInfo = parseDecision(methodText)
                    fightmethod = parsedDecisionInfo[0].strip()
                    fightmethodspecific = parsedDecisionInfo[1].strip(
                    ).capitalize()
                    judgescore1 = parsedDecisionInfo[2].strip()
                    judgescore2 = parsedDecisionInfo[3].strip()
                    judgescore3 = parsedDecisionInfo[4].strip()
                else:
                    parsedFinishInfo = parseFinish(methodText)
                    fightmethod = parsedFinishInfo[0].strip()
                    fightmethodspecific = parsedFinishInfo[1].strip(
                    ).capitalize()

                if fightmethod == 'NC' or fightmethod == 'No Contest':
                    isnocontest = 1

                if (methodText.find('Draw') > -1):
                    isdraw = 1

                fightResult = {
                    'isdraw': isdraw,
                    'isnocontest': isnocontest,
                    'winnername': winnername,
                    'losername': losername,
                    'fightmethod': fightmethod,
                    'fightmethodspecific': fightmethodspecific,
                    'judgescore1': judgescore1,
                    'judgescore2': judgescore2,
                    'judgescore3': judgescore3,
                    'round': round,
                    'time': time,
                    'notes': notes,
                    'eventname': eventname
                }
                cardSections[curCardSectionIndex]['fights'].append(fightResult)
    for section in cardSections:
        i = 0
        for fight in section['fights']:
            fight['cardsectionid'] = i
            # response = requests.post(
            #     'https://zdcdh4dtx0.execute-api.us-east-1.amazonaws.com/prd/fight', json=fight)
            # print(f"Posted fight: {response.status_code}")
            # print(response.text)
            i += 1
    return cardSections


def postNewEventInfo(eventname):
    card = getCardInfo(eventname)
    for section in card:
        print(section['title'])
        for fight in section['fights']:
            response = requests.post(
                'https://zdcdh4dtx0.execute-api.us-east-1.amazonaws.com/prd/fight', json=fight)
            print(f"Posted fight: {response.status_code}")


def main():
    latestEventName = getLatestEventName()
    card = getCardInfo('UFC Fight Night: Tsarukyan vs. Hooker')
    for section in card:
        # print(section['title'])
        for fight in section['fights']:
            # print(fight)
            if fight['winnername'] == 'Kyoji Horiguchi':
                response = requests.post(
                    'https://zdcdh4dtx0.execute-api.us-east-1.amazonaws.com/prd/fight/result', json=fight)
                print(f"Posted fight: {response.status_code}")
                print(response.text)


if __name__ == '__main__':
    main()
