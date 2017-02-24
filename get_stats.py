#!/usr/bin/env python
import json
from collections import Counter

n_templates = 0
n_examples = 0
semantics = Counter()
example_per_template = Counter()
n_slots = Counter()
n_gui = Counter()
n_guitag = 0
has_answers = 0
for entry in open('data/combined.jsonl'):
    n_templates += 1
    entry = json.loads(entry)
    semantics[entry['semantic']] += 1
    dat = entry['data']
    example_per_template[len(dat)] += 1 
    n_examples += len(dat)
    if 'ANSWER' in dat[0]:
        n_slots[len(dat[0]) - 1] += 1
        if len(dat[0]) == 7: print(entry['question'])
    else:
        n_slots[len(dat[0])] += 1
        if len(dat[0]) == 6: print(entry['question'])
    for d in dat:
        if 'ANSWER' in d:
            has_answers += 1
    if 'gui' in entry:
        n_gui.update(entry['gui'])
        n_guitag += 1

print('n_templates', n_templates)
print('n_examples', n_examples)
print('has_answers', has_answers)
print('Semantics')
for k, count in semantics.most_common():
    print('\t', k, '=', count)
print('Example per template')
for k, count in example_per_template.most_common():
    print('\t', k, '=', count)
print('Number of slots')
for k, count in n_slots.most_common():
    print('\t', k, '=', count)
print('{} entries have GUI tags'.format(n_guitag))
for k, count in n_gui.most_common():
    print('\t', k, '=', count)
