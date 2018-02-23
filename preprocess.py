#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re 
from aylienapiclient import textapi
import requests

def microsoft(text):
	subscription_key="5d162a1f02724f6daf4489f4220413a4"
	text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"

	documents = {'documents' : [
	  {'id': '1', 'language': 'en', 'text': text}
	]}

	# Get Langauge
	language_api_url = text_analytics_base_url + "languages"
	headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
	response  = requests.post(language_api_url, headers=headers, json=documents)
	languages = response.json()['documents'][0]['detectedLanguages'][0]['name']
	

	# Get Sentiment
	sentiment_api_url = text_analytics_base_url + "sentiment"
	headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
	response  = requests.post(sentiment_api_url, headers=headers, json=documents)
	sentiments = response.json()['documents'][0]['score']

	# Get Keywords
	key_phrase_api_url = text_analytics_base_url + "keyPhrases"
	headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
	response  = requests.post(key_phrase_api_url, headers=headers, json=documents)
	key_phrases = response.json()['documents'][0]['keyPhrases']

	return key_phrases,sentiments,languages

def get_summary(text):
    c = textapi.Client("f5123f5c", "15e79b1e3a7e384e46d09665eef5707f")
    aylien_options = {
        'title': 'transcripts-part',
        'text': text,
        'sentences_number': 4,
        'language': 'en'

    }
    result = c.Summarize(aylien_options)
    return result['sentences']

def get_sentiment(text):
    client = textapi.Client("f5123f5c", "15e79b1e3a7e384e46d09665eef5707f")
    sentiment = client.Sentiment({'text': text})
    print(sentiment)


clientName='KEVIN'
clientMessages = []

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
            if not re.search(r"(why dont you (go first|go next|start|begin)|(tell me|what are) your updates)|lets talk about your task|you are up next", str(msg.lower())) == None:
                #print (re.search(r"(why dont you (go first|start|begin)| tell me your updates)", str(msg)))
                if startRecording == -1:
                    startRecording = index
                    nextSpeakerAssignFlag = True
                else:
                    stopRecording = index
                    break

            # End Regular expression
            if not re.search(r"Thats (it|all) (from my (updates|end|side)|the day)", str(msg)) == None:
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
            if message['name'] == clientName:
                clientMessages.append(message['message'].encode("ascii", "ignore"))
    
    return wordsSpoken,lastStopRecording

lastStopRecording = 0
while True:
    wordsSpoken,lastStopRecording = getSpeakerTask(lastStopRecording-1)

    if lastStopRecording == None:
        break

    print(wordsSpoken)
    print('========================== SUMMARY ===========================')
    summary = get_summary(''.join(wordsSpoken))
    print summary
    print "------------"
    get_sentiment(''.join(summary))
    print "------------"
    MicrosoftKeyPhrases,MicrosoftSentiments,MicrosoftLanguages = microsoft(''.join(summary))
    print MicrosoftSentiments
    print('==============================================================')



print (clientMessages)
summary = get_summary(''.join(clientMessages))
print ''.join(summary)
print "------------"
get_sentiment(''.join(summary))

MicrosoftKeyPhrases,MicrosoftSentiments,MicrosoftLanguages = microsoft(''.join(summary))
print MicrosoftSentiments


