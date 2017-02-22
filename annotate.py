"""
Annotate questions by:

- Difficulty: 0=good, 1=bad question good website, 2=impossible

- Tags:
    s=search
    t=text
    d=date
    dr=dropdown
    sc=scroll
    sp=special control (plus/minus)
    c=click

- Semantics:
    t=transportation (flight, railway, bus)
    h=housing (hotel, real estate)
    s=shopping
    d=dining
    e=entertainment (movie, event)
    c=calculator
    o=other
"""
import sys
import json
import webbrowser
import pyperclip

QuestionFile = 'data/level1.jsonl'
FriendlyCode = 'data/mobile_friendly_code.txt'
AnnotationFile = 'data/raw_annotation.csv'
Start = 53

def write(line):
    with open(AnnotationFile, 'a') as ann:
        ann.write(line + '\n')
        ann.flush()

friendly_code = set(map(str.strip, open(FriendlyCode).readlines()))

i = 0
for line in open(QuestionFile):
    D = json.loads(line)
    code = D['code']
    if code not in friendly_code:
        continue
    if D['url'].lower() == 'test':
        continue
    
    i += 1
    if i < Start:
        continue

    question0 = D['question']
    print(code)
    print(D['url'])
    for entry in D['data']:
        question = question0
        for k, v in entry.items():
            question = question.replace('({})'.format(k), v)
        print(question)

#     webbrowser.open(D['url'], new=0)
    pyperclip.copy(D['url'])
    gui = input('GUI tag: ')
    gui = '|'.join(gui.split())
    semantics = input('Semantic tag: ')
    semantics = '|'.join(semantics.split())
    if gui == '-':
        difficulty = '2'
        semantics = '-'
    elif gui == '#':
        difficulty = '1'
        gui = '-'
        semantics = '-'
    else:
        difficulty = '0'
    entry = ', '.join([code, difficulty, gui, semantics])
    write(entry)
    print('-'*10, '\n')