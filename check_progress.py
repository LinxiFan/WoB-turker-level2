#!/usr/bin/env python
"""
-s: connect to ssh
"""
import os
import json
import sys
from urllib.request import urlretrieve

AWS = 'ec2-52-33-170-48.us-west-2.compute.amazonaws.com'

if len(sys.argv) > 1:
    os.system('ssh -i wob_openai.pem ubuntu@'+AWS)
    sys.exit(0)


HTTP = 'http://{}:8080/data/{}'
urlretrieve(HTTP.format(AWS, 'level2.jsonl'), filename='data/level2.jsonl')
urlretrieve(HTTP.format(AWS, 'progress.json'), filename='data/progress.json')

progress = json.load(open('data/progress.json'))
total = 0
i = 0
for code, val in progress.items():
    if val > 0:
        print(code, '+', val)
        total += val
    if val > 100:
        i +=1
print('Total HITs:', total)
print(i)
os.system('wc -l data/level2.jsonl')
# os.system('less data/level2.jsonl')