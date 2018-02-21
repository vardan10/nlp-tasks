#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re 

def chopData():
    startRecording = 0
    stopRecording = 0
    speaker = ''

    with open('input.json') as data_file:    
        for index,message in enumerate(json.load(data_file)['transcript']):
            
            # Remove non-ascii caracters
            msg = message['message'].encode("ascii", "ignore")

            if index == startRecording + 1:
                speaker = message['name']

            # Start Regular expression
            if not re.search(r"(why dont you (go first|start|begin)| tell me your updates)", str(msg)) == None:
                #print (re.search(r"(why dont you (go first|start|begin)| tell me your updates)", str(msg)))
                startRecording = index

            # End Regular expression
            if not re.search(r"Thats (it|all) from my (end|side)", str(msg)) == None:
                #print (re.search(r"Thats (it|all) from my (end|side)", str(msg)))
                stopRecording = index
    
    if not stopRecording == 0:
        return speaker,startRecording,stopRecording
    else:
        return None,None,None

def getSpeakerTask():
    wordsSpoken = []
    speaker,startRecording,stopRecording = chopData()

    with open('input.json') as data_file:
        for index,message in enumerate(json.load(data_file)['transcript'][startRecording+1:stopRecording+1]):
            if message['name'] == speaker:
                wordsSpoken.append(message['message'].encode("ascii", "ignore"))
    
    return wordsSpoken

wordsSpoken = getSpeakerTask()
print(wordsSpoken)
print(len(wordsSpoken))