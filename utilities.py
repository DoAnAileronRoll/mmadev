def parseDecision (text):
    textList = text.replace('(', '').replace(')','').replace(',','').split(' ')
    if len(textList) == 2: 
        textList.extend(['','',''])
    return textList 
#TKO (spinning back elbow and punches)	
def parseFinish (text):
    return text.replace(')','').split('(')

#TKO (spinning back elbow and punches)	
def parseNoContest (text):
    return text.replace(')','').split('(')

def parseWeight (text):
    if(text.find('lb)') > -1):
        splitted = text.replace(')','').split('(')
        return [splitted[0].strip(),splitted[1].strip()]
    return [text, None]
