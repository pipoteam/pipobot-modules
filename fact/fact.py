# -*- coding: utf-8 -*-

# $ python3 fact.py furet mort
# De tout. Al Qaeda, les furets, les édulcorants artificiels, les distributeurs de bonbons PEZ avec leurs yeux de mort.
# $ python3 fact.py furet
# Des manipulations quotidiennes pendant ce stade critique du développement sont indispensables au comportement social du furet adulte.

import re

import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Host': 'context.reverso.net',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'}
api = 'http://context.reverso.net/bst-query-service?source_text={txt}&source_lang={src}&target_lang={dst}&npage=1&json=1&nrows=20'


def fact(txt):
    query = {'txt': txt, 'src': 'fr', 'dst': 'en'}
    for key, item in query.items():
        query[key] = requests.utils.quote(item.encode('utf-8'))

    r = requests.get(api.format(**query), headers=headers)
    if r.status_code != 200:
        return []

    em = re.compile(r'.*<em>.*</em>.*')
    results = r.text.split('"')
    results = [res for res in results if em.match(res)]

    best = max([res.count('<') for res in results])
    results = [res for res in results if res.count('<') == best]

    results.sort(key=lambda val: len(val))
    return results[-1].replace('<em>', '').replace('</em>', '')
