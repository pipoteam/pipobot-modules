# $ python3 translate.py fr en furet mort
# [('mort', 'out'), ('furets', 'ferrets'), ('mort', 'dead'), ('furet', 'ferret'), ('mort', 'died'), ('furets mort', 'lemming death panels'), ('mort', 'death')]
# $ python3 translate.py fr es furet mort
# [('mort', 'muerte'), ('furet', 'hurones'), ('furet', 'hurón'), ('mort', 'murió'), ('furet', 'hurón tiene'), ('mort', 'muertos'), ('mort', 'irse'), ('mort', 'muerto')]

import requests
import sys
import re

src = sys.argv[1]
dst = sys.argv[2]
words = sys.argv[3:]

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'en-US,en;q=0.5',
'Connection': 'keep-alive',
'Host': 'context.reverso.net',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'}
api = 'http://context.reverso.net/bst-query-service?source_text={txt}&source_lang={src}&target_lang={dst}&npage=1&json=1&nrows=20'

def translate(txt, src, dst):
    query = {'txt': txt, 'src': src, 'dst': dst}
    for key, item in query.items():
        query[key] = requests.utils.quote(item)

    r = requests.get(api.format(**query), headers=headers)
    if r.status_code != 200:
        return []

    em = re.compile(r'^[^<]*<em>([^<]*)</em>(.*)$')
    results = r.text.split('"')

    ind = 0
    bins = []
    remains = results
    while len(remains) > 0:
        bins += [em.match(remain).group(1).lower() for remain in remains if em.match(remain)]
        remains = [em.match(remain).group(2).lower() for remain in remains if em.match(remain)]
    results = [tuple(bins[i:i+2]) for i in range(0, len(bins), 2)]
    return list(set(results))

tr = []
for word in words:
    tr += translate(word, src, dst)
if len(words) > 1:
    tr += translate(' '.join(words), src, dst)
tr = list(set(tr))

print(tr)
