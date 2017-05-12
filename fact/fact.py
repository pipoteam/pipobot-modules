# -*- coding: utf-8 -*-

# $ python3 fact.py furet mort
# De tout. Al Qaeda, les furets, les édulcorants artificiels, les distributeurs de bonbons PEZ avec leurs yeux de mort.
# $ python3 fact.py furet
# Des manipulations quotidiennes pendant ce stade critique du développement sont indispensables au comportement social du furet adulte.

import re

import requests
import random
import sys

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Host': 'context.reverso.net',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'}
api = 'http://context.reverso.net/bst-query-service?source_text={txt}&source_lang={src}&target_lang={dst}&npage=1&json=1&nrows=20'

def quote(c, txt, lang):
    query = {'txt': txt, 'src': lang, 'dst': 'en'}
    for key, item in query.items():
        try:
            query[key] = requests.utils.quote(item.encode('utf-8'))
        except UnicodeDecodeError:
            query[key] = requests.utils.quote(item)

    r = requests.get(api.format(**query), headers=headers)
    if r.status_code != 200:
        return []

    em = re.compile(r'.*<em>.*</em>.*')
    results = r.text.split('"')
    results = [r for r in results if em.match(r)]
    results = results[::2]

    if len(results) < 1:
        return []

    best = max([r.count('<') for r in results])
    results = [r for r in results if r.count('<') == best]
    results = [r.replace('<em>', '').replace('</em>', '') for r in results]

    if len([r for r in results if r in c.buff]) > 0:
        random.shuffle(results)
    else:
        results.sort(key=lambda val: len(val))
    return results

def fetchfact(c, argv):
    line = []
    lang = c.lang
    for l in argv:
        if l.startswith('-'):
            lang = l[1:]
        else:
            line.append(l)
    res = quote(c, ' '.join(line), lang)

    while len(res) > 1 and res[-1] in c.buff:
        res.pop()
    if len(res) < 1:
        return []

    c.buff.append(res[-1])
    if len(c.buff) > c.size:
        c.buff.pop(0)
    return res[-1]

def pickfact(c):
    if len(c.buff) < 1:
        return c.fall

    last = None
    tries = 0
    while last is None and tries < 5:
        tries += 1
        line = ''
        try:
            line = random.sample(c.buff, 1)
        except:
            return c.fall

        try:
            args = [w for w in line.split() if len(w) > 3]
            last = ' '.join(random.sample(args, 2))
        except:
            last = None
    if last is None or len(last) < 1:
        return c.fall

    return last

def fact(c, txt):
    word = ''
    tries = 0
    while len(word) < 1 and tries < 5:
        tries += 1
        if len(txt) < 2:
            txt = c.last
        word = fetchfact(c, txt.split())
        txt = ''

        try:
            c.last = ' '.join(random.sample(word.split(), 2))
        except:
            c.last = pickfact(c)
    if word is None or len(word) < 1:
        return c.fall

    return word
