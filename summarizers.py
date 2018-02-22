#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from aylienapiclient import textapi

regex_start = r"you\s*(go|start|begin|give|are\s*(are))+"
regex_end = r"my\s*(end|update|updates)+"

def __get_summary(text):
    c = textapi.Client("f5123f5c", "15e79b1e3a7e384e46d09665eef5707f")
    aylien_options = {
        'title': 'transcripts-part',
        'text': text,
        'sentences_number': 4,
        'language': 'en'

    }
    result = c.Summarize(aylien_options)
    return result['sentences']


def get_summmaries(content):

    summaries =[]
    content_length = len(content)
    catch_first_pos = 0;
    catch_last_pos = content_length


    catch_first = re.search(regex_start, content, re.MULTILINE)
    catch_last = re.search(regex_end, content, re.MULTILINE)

    if catch_first is None and catch_last is None:
        summaries = [__get_summary(content)]

    else:
        next = content
        while catch_first is not None:
            catch_first_pos = catch_first.start()
            if catch_last is not None:
             catch_last_pos = catch_last.end()
            else:
             catch_last_pos = content_length
            section = next[catch_first_pos:catch_last_pos]
            summaries.append(__get_summary(section))
            next = content[catch_last_pos:content_length]
            catch_first = re.search(regex_start, next, re.MULTILINE)
            catch_last = re.search(regex_end, next, re.MULTILINE)

    return summaries

file = open('transcripts-part.txt', 'r')
print get_summmaries(file.read())