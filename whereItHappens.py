import wikipedia
from bs4 import BeautifulSoup
from utilities import * 
from getEventNames import getEventNames

def main():
    result = wikipedia.page("UFC 12") 
    html = result.html()

    soup = BeautifulSoup(html, features='html.parser')
    table = soup.find('table', attrs={'class':'toccolours', 'style': 'font-size: 85%;'})
    tableBody = table.find('tbody')

    cardSections = []

    for index, row in enumerate(tableBody.find_all('tr')):
        allHeadersInRow = row.find_all('th')
        if(len(allHeadersInRow) == 1):
            cardSections.append({
                'title': allHeadersInRow[0].text.strip(),
                'fights': []
            })
        elif(len(allHeadersInRow) == 0): 
            vals = row.find_all('td')
            weightInfo = parseWeight(vals[0].text.strip())
            fightInfo = {
                'WeightClass': weightInfo[0],
                'CatchweightLimit': weightInfo[1],
                'Fighter1': vals[1].text.strip(),
                'Fighter2': vals[3].text.strip(),
                'Winner': '',
                'Method': '',
                'MethodSpecific': '',
                'JudgeScore1': '',
                'JudgeScore2': '',
                'JudgeScore3': '',
                'Round': vals[5].text.strip(),
                'Time': vals[6].text.strip(),
                'Notes': ''    
            }
            methodText = vals[4].text.strip()
            fightInfo['Winner'] = 1 if vals[2].text.strip() == 'def.' else 0

            if(methodText.find('Decision') > -1 or methodText.find('Draw') > -1):
                    parsedDecisionInfo = parseDecision(methodText)
                    fightInfo['Method'] = parsedDecisionInfo[0].strip()
                    fightInfo['MethodSpecific'] = parsedDecisionInfo[1].strip().capitalize()
                    fightInfo['JudgeScore1'] = parsedDecisionInfo[2].strip() 
                    fightInfo['JudgeScore2'] = parsedDecisionInfo[3].strip()
                    fightInfo['JudgeScore3'] = parsedDecisionInfo[4].strip()
            else:
                parsedFinishInfo = parseFinish(methodText)
                fightInfo['Method'] = parsedFinishInfo[0].strip()
                fightInfo['MethodSpecific'] = parsedFinishInfo[1].strip().capitalize()

            cardSections[-1]['fights'].append(fightInfo)
    for section in cardSections:
        print(section['title'])
        for fight in section['fights']:
            print(fight.values())

if __name__ == '__main__':
    main()
    