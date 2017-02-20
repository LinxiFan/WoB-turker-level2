#!/usr/bin/env python
import json

level1_json = 'data/level1.jsonl'
level2_json = 'data/level2.jsonl'
annotation = 'data/annotation.jsonl'
output_json = 'data/combined.jsonl'
# ====================================
level1DB = map(json.loads, open(level1_json).readlines())
level1DB = {entry['code']: entry for entry in level1DB}
annotation = map(json.loads, open(annotation).readlines())
annotation = {entry['code']: entry for entry in annotation}

combinedDB = {}

for l2 in open(level2_json):
    l2 = json.loads(l2)
    code = l2['code1']
    if code in combinedDB:
        combinedDB[code]['data'].extend(l2['data'])
    else:
        entry = {}
        for tag in ['code', 'url', 'question', 'data']:
            entry[tag] = level1DB[code][tag]
        for tag in ['gui', 'difficulty', 'semantic']:
            entry[tag] = annotation[code][tag]
        combinedDB[code] = entry

with open(output_json, 'w') as f:
    for code, entry in combinedDB.items():
        print(json.dumps(entry), file=f)