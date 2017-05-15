# -*- coding: utf-8 -*-

import random
import re

from pipobot.lib.module_test import ModuleTest
from pipobot.lib.modules import SyncModule, defaultcmd

import requests

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Host': 'context.reverso.net',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
}

API = 'http://context.reverso.net/bst-query-service'


class CmdQuote(SyncModule):
    '''Retrieve a sentence from reverso.net, matching keywords and a language.

    Configuration keys:
        - lang: Define the default language used to retrieve the "quotes"/"facts".
        - size: Define the history size (the bot tries to doesn't repeat itself).
        - fall: Define the fallback keyword used when no history is available.'''
    _config = (("lang", str, "fr"), ("size", int, 256), ("fall", str, "fr"))

    def __init__(self, bot):
        desc = _('fact <txt> [lang]: find a fact with <txt> (in [lang]) on reverso.net')
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name='fact')
        self.last = self.fall
        self.buff = []

    def quote(self, txt, lang):
        query = {'source_text': txt, 'source_lang': lang, 'target_lang': 'en', 'npage': 1, 'json': 1, 'nrows': 20}
        ret = requests.get(API, query, headers=HEADERS)
        if ret.status_code != 200:
            return []

        em = re.compile(r'.*<em>.*</em>.*')
        results = ret.text.split('"')
        results = [r for r in results if em.match(r)]
        results = results[::2]

        if len(results) < 1:
            return []

        best = max([r.count('<') for r in results])
        results = [r for r in results if r.count('<') == best]
        results = [r.replace('<em>', '').replace('</em>', '') for r in results]

        if len([r for r in results if r in self.buff]) > 0:
            random.shuffle(results)
        else:
            results.sort(key=lambda val: len(val))
        return results

    def fetchfact(self, argv):
        line = []
        lang = self.lang
        for l in argv:
            if l.startswith('-'):
                lang = l[1:]
            else:
                line.append(l)
        res = self.quote(' '.join(line), lang)

        while len(res) > 1 and res[-1] in self.buff:
            res.pop()
        if len(res) < 1:
            return []

        self.buff.append(res[-1])
        if len(self.buff) > self.size:
            self.buff.pop(0)
        return res[-1]

    def pickfact(self):
        if len(self.buff) < 1:
            return self.fall

        last = None
        tries = 0
        while last is None and tries < 5:
            tries += 1
            line = ''
            try:
                line = random.sample(self.buff, 1)
            except:
                return self.fall

            try:
                args = [w for w in line.split() if len(w) > 3]
                last = ' '.join(random.sample(args, 2))
            except:
                last = None
        if last is None or len(last) < 1:
            return self.fall

        return last

    @defaultcmd
    def fact(self, sender, txt):
        word = ''
        tries = 0
        while len(word) < 1 and tries < 5:
            tries += 1
            if len(txt) < 2:
                txt = self.last
            word = self.fetchfact(txt.split())
            txt = ''

            try:
                self.last = ' '.join(random.sample(word.split(), 2))
            except:
                self.last = self.pickfact()
        if word is None or len(word) < 1:
            return self.fall

        return word


class QuoteTest(ModuleTest):
    def test_fact(self):
        rep = self.bot_answer('!fact furet mort')
        self.assertEqual(rep[:77], 'De tout. Al Qaeda, les furets, les édulcorants artificiels, les distributeurs')
        rep = self.bot_answer('!fact furet')
        self.assertEqual(rep[:73], 'Des manipulations quotidiennes pendant ce stade critique du développement')
        rep = self.bot_answer('!fact chargé')
        self.assertEqual(rep[:71], u'Plus pr\xe9cis\xe9ment, le porteur charg\xe9 positivement est un polypeptide cha')
