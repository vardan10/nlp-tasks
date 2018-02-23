#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re 

def chopData(lastStopRecording,finished):
    issueStart = -1
    issueStop = -1

    with open('input.json') as data_file:    
        for index,message in enumerate(json.load(data_file)['transcript'][lastStopRecording+1:]):

            # Remove non-ascii caracters
            msg = message['message'].encode("ascii", "ignore")

            # Start Regular expression
            if not re.search(r"(defect|task|issue)(.{0,8}| number) \d+", str(msg.lower())) == None:
                
                if issueStart == -1:
                    issueStart = index
                else:
                    issueStop = index - 1
                    break
    
    if not issueStop == -1:
        return issueStart+lastStopRecording+1,issueStop+lastStopRecording+1
    elif finished == True and not issueStart == -1:
        return issueStart+lastStopRecording+1,None
    else:
        return None,None

            




lastStopIssue = -1
while True:
    issueStart,issueStop = chopData(lastStopIssue,False)
    
    if issueStart == None:
        print(chopData(lastStopIssue,True))
        break

    print(issueStart,issueStop)
    lastStopIssue = issueStop - 1

