#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re 


def chopData(lastStopRecording):
    startRecording = -1
    stopRecording = -1
    speaker = ''
    nextSpeakerAssignFlag = False

    with open('input.json') as data_file:    
        for index,message in enumerate(json.load(data_file)['transcript'][lastStopRecording+1:]):
            
            # Remove non-ascii caracters
            msg = message['message'].encode("ascii", "ignore")

            # print (msg)

            # Get Speaker Name
            if nextSpeakerAssignFlag:
                nextSpeakerAssignFlag = False
                speaker = message['name']

            # Start Regular expression
            if not re.search(r"(why dont you (go first|go next|start|begin)| tell me your updates)", str(msg)) == None:
                #print (re.search(r"(why dont you (go first|start|begin)| tell me your updates)", str(msg)))
                if startRecording == -1:
                    startRecording = index
                    nextSpeakerAssignFlag = True
                else:
                    stopRecording = index
                    break

            # End Regular expression
            if not re.search(r"Thats (it|all) from my (end|side)", str(msg)) == None:
                #print (re.search(r"Thats (it|all) from my (end|side)", str(msg)))
                stopRecording = index + 1
                speaker = message['name']
                break

    if not stopRecording == -1:
        if startRecording == -1:
            startRecording = lastStopRecording + 1
        
        
        startRecording = startRecording + lastStopRecording + 1
        stopRecording = stopRecording + lastStopRecording + 1
        lastStopRecording = stopRecording
        print(speaker,startRecording,stopRecording,lastStopRecording)
        
        return speaker,startRecording,stopRecording,lastStopRecording
    else:
        return None,None,None,None



def getSpeakerTask(lastStopRecording):
    wordsSpoken = []
    speaker,startRecording,stopRecording,lastStopRecording = chopData(lastStopRecording)
    if speaker == None:
        return None,None

    with open('input.json') as data_file:
        for index,message in enumerate(json.load(data_file)['transcript'][startRecording+1:stopRecording+1]):
            if message['name'] == speaker:
                wordsSpoken.append(message['message'].encode("ascii", "ignore"))
    
    return wordsSpoken,lastStopRecording

lastStopRecording = 1
while True:
    wordsSpoken,lastStopRecording = getSpeakerTask(lastStopRecording-1)
    
    print(wordsSpoken)
    print('==============================================================')

    if lastStopRecording == None:
        break