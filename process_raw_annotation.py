"""
Process `raw_annotation.csv` into `annotation.jsonl`
"""
import json

RawFile = 'data/raw_annotation.csv'
ProcessedFile = 'data/annotation.jsonl'

GUI = {
    's': 'search',
    't': 'text',
    'd': 'date',
    'm': 'menu',
    'dr': 'dropdown',
    'sc': 'scroll',
    'sp': 'special',
    '-': '-',
    '#': '-'
}

Semantic = {
    't': 'transportation',
    'h': 'housing',
    's': 'shopping',
    'd': 'dining',
    'e': 'entertainment',
    'c': 'calculator',
    'o': 'other',
    '-': '-',
    '#': '-'
}
# ===================================================
ProcessedFile = open(ProcessedFile, 'w')


for line in open(RawFile):
    code, difficulty, gui, semantic = map(str.strip, line.strip().split(','))
    gui = gui.split('|')

    dat = {
        'code': code,
        'difficulty': int(difficulty),
        'gui': list(map(GUI.get, gui)),
        'semantic': Semantic[semantic]
    }
    print(json.dumps(dat), file=ProcessedFile)

ProcessedFile.close()