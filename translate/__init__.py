# -*- coding: utf-8 -*-

from pipobot.lib.module_test import ModuleTest
from pipobot.lib.modules import SyncModule, answercmd, defaultcmd

from .translate import translate


class CmdTranslate(SyncModule):
    desc = _('translate <src> <dst> <txt>: ask reverso.net to translate <txt> from <src> to <dst>')

    def __init__(self, bot):
        SyncModule.__init__(self,
                            bot,
                            desc=self.desc,
                            name='translate')

    @answercmd(r'(?P<src>[^ ]+) (?P<dst>[^ ]+) (?P<txt>.*)')
    def translate(self, sender, src, dst, txt):
        words = txt.split()
        tr = []
        for word in words:
            tr += translate(word, src, dst)
        if len(words) > 1:
            tr += translate(' '.join(words), src, dst)

        ret = {}
        for key, value in tr:
            if key in ret:
                ret[key].append(value)
            else:
                ret[key] = [value]

        return ['%s: %s' % (key, ', '.join(values)) for key, values in ret.items()]

    @defaultcmd
    def answer_desc(self, sender, message):
        return self.desc


class TranslateTest(ModuleTest):
    def test_translate(self):
        rep = self.bot_answer('!translate fr en furet mort')
        self.assertIn('furets mort: lemming death panels', rep)
        rep = self.bot_answer('!translate fr es furet mort')
        self.assertIn('furets: hurones', rep)

    def test_desc(self):
        rep = self.bot_answer('!translate pipo')
        self.assertEqual(rep, CmdTranslate.desc)
