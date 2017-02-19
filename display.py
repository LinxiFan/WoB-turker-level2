import json
import sys

for line in open(sys.argv[1]):
    D = json.loads(line)
    if D['url'].lower() == 'test':
        continue
    question0 = D['question']
    print(D['url'])
    for entry in D['data']:
        question = question0
        for k, v in entry.items():
            question = question.replace('({})'.format(k), v)
        if 'ANSWER' in entry:
            ans = '-> ' + entry['ANSWER']
        else:
            ans = ''
        print(question, ans)
    print('-'*10)
