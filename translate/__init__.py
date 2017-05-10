# -*- coding: utf-8 -*-

from pipobot.lib.modules import SyncModule, defaultcmd, answercmd
from pipobot.lib.module_test import ModuleTest

from translate.translate import translate


class CmdTranslate(SyncModule):
    def __init__(self, bot):
        desc = _('translate <src> <dst> <txt>: ask reverso.net to translate <txt> from <src> to <dst>')
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name='translate')

    @answercmd(r'(?P<src>[^ ]+) (?P<dst>[^ ]+) (?P<txt>.*)')
    def translate(self, sender, src, dst, txt):
        words = txt.split()
        tr = []
        for word in words:
            tr += translate(word, src, dst)
        if len(words) > 1:
            tr += translate(' '.join(words), src, dst)
        tr = list(set(tr))

        return str(tr)

    @defaultcmd
    def desc(self, sender, message):
        return self.desc


class TranslateTest(ModuleTest):
    def test_translate(self):
        rep = self.bot_answer('!translate fr en furet mort')
        self.assertEqual(rep[:58], "[('mort', 'out'), ('furets', 'ferrets'), ('mort', 'dead'),")
        rep = self.bot_answer('!translate fr es furet mort')
        self.assertEqual(rep[:62], "[('mort', 'muerte'), ('furet', 'hurones'), ('furet', 'hurón'),")

    def test_desc(self):
        rep = self.bot_answer('!translate pipo')
        self.assertEqual(rep, CmdTranslate.desc)
