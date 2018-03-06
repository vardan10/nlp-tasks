import json
import datetime

words = []
firstTimestamp = None

data = json.load(open('1.json'))
startTimestamp = datetime.datetime.fromtimestamp(data['startTimestamp'])

if firstTimestamp == None:
    firstTimestamp = startTimestamp

for word in data['words']:
    wordStartTime = float(word['startTime'][:-1])
    wordTime = startTimestamp + datetime.timedelta(seconds=wordStartTime)
    CorrectTime = wordTime - firstTimestamp
    words.append({"word":word['word'],"time": CorrectTime })

print words