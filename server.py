from tornado import (ioloop, web)
import hashlib
import random
import os
import json

DEBUG = False
MAX_EXAMPLE = 25 if DEBUG else 100 # how many instantiations do we want per template?

progress_json = 'test_progress.json' if DEBUG else 'progress.json'
level1_json = 'test_level1.jsonl' if DEBUG else 'level1.jsonl'
level2_json = 'test_level2.jsonl' if DEBUG else 'level2.jsonl'
annotation = 'test_annotation.jsonl' if DEBUG else  'annotation.jsonl'

PORT = 8080
# =======================================================

templateDB = {}
progress_json = os.path.join('data', progress_json)
level1_json = os.path.join('data', level1_json)
level2_json = os.path.join('data', level2_json)
annotation = os.path.join('data', annotation)

if os.path.exists(progress_json):
    with open(progress_json) as f:
        progress = json.load(f)
else:
    progress = {}


good_code = set()
for line in open(annotation):
    entry = json.loads(line)
    if entry['difficulty'] == 0:
        good_code.add(entry['code'])

for line in open(level1_json):
    entry = json.loads(line)
    code = entry['code']
    if (code not in good_code
        or entry['url'].lower() == 'test'):
        continue
    entry['question'] = entry['question'].replace('\n', ' ')
    templateDB[code] = entry
    if code not in progress:
        progress[code] = 0

print('# Number of good code:', len(good_code))

unfinished_pool = []
for code in progress:
    if progress[code] < MAX_EXAMPLE:
        unfinished_pool.append(code)


def update_progress(code, addition, save=True):
    global progress
    assert code in progress
    progress[code] += addition
    print('# Progress {} +{}'.format(code, addition))
    if save:
        with open(progress_json, 'w') as f:
            json.dump(progress, f)


def sample_level1():
    "Return a random template and update unfinished_pool"
    global unfinished_pool
    while unfinished_pool:
        code = random.sample(unfinished_pool, 1)[0]
        if progress[code] >= MAX_EXAMPLE:
            unfinished_pool.remove(code)
        else:
            print('# sample:', code)
            return templateDB[code]
    return None


def instantiate(entry, N=5):
    "Instantiate a template with concrete blanks"
    assert N < len(entry['data'])
    question = entry['question']
    blanks = random.sample(entry['data'], N)
    examples = []
    for blank in blanks:
        q = question
        for key, val in blank.items():
            q = q.replace(u'({})'.format(key), u'<u>{}</u>'.format(val))
        examples.append(q)
    return examples
        

def update_level2db(dat):
    with open(level2_json, 'a') as f:
        print(dat, file=f)
    print(dat)


def wrap_template(html_template):
    class TemplateHandler(web.RequestHandler):
        def get(self):
            entry = sample_level1()
            if entry is None:
                print('# DONE!!!!!!')
                self.render(html_template, done=True)
                return
            
            url = entry['url']
            if not url.startswith('http'):
                url = 'http://' + url
            self.render(html_template, 
                        url=url, 
                        question=entry['question'],
                        code1=entry['code'],
                        blanks=' and '.join(map('[{}]'.format, entry['data'][0].keys())),
                        examples=instantiate(entry, 5),
                        done=False,
                        debug=DEBUG)
    return TemplateHandler


class SubmitHandler(web.RequestHandler):
    def post(self):
        data = json.loads(self.get_argument('data'))
        url = self.get_argument('url')
        question = json.loads(self.get_argument('question'))
        code1 = self.get_argument('code1')
        code2 = self.get_argument('code2')

        recv = json.dumps({
            'data': data,
            'url': url,
            'question': question,
            'code1': code1,
            'code2': code2
        })
        update_level2db(recv)
        update_progress(code1, 10)
        self.write('OK')


handlers = [
    (r"/", wrap_template('index.html')),
    (r"/submit", SubmitHandler),
    (r"/(.*\.js)", web.StaticFileHandler, {"path": "./"}),
    (r"/(.*\.css)", web.StaticFileHandler, {"path": "./"}),
    (r"/(.*\.html)", web.StaticFileHandler, {"path": "./"}),
    (r"/(.*\.jsonl)", web.StaticFileHandler, {"path": "./"}),
    (r"/(.*\.json)", web.StaticFileHandler, {"path": "./"}),
]

settings = {
    "autoreload": True,
    "debug": True,
    "template_path": "./",
}

if __name__ == "__main__":
    # start main application.
    application = web.Application(handlers, **settings)
    port = int(os.environ.get("PORT", PORT))
    application.listen(port, address="0.0.0.0")
    print('# localhost:{}'.format(PORT))
    ioloop.IOLoop.current().start()
