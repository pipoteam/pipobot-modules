# -*- coding: utf-8 -*-

from pipobot.lib.module_test import ModuleTest
from pipobot.lib.modules import SyncModule, defaultcmd
from quote.quote import quote


class CmdQuote(SyncModule):
    def __init__(self, bot):
        desc = _('quote <txt>: find a quote with <txt> on reverso.net')
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name='quote')

    @defaultcmd
    def answer(self, sender, message):
        return quote(message)


class QuoteTest(ModuleTest):
    def test_quote(self):
        rep = self.bot_answer('!quote furet mort')
        self.assertEqual(rep[:77], 'De tout. Al Qaeda, les furets, les édulcorants artificiels, les distributeurs')
        rep = self.bot_answer('!quote furet')
        self.assertEqual(rep[:73], 'Des manipulations quotidiennes pendant ce stade critique du développement')
