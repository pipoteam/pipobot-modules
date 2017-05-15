# -*- coding: utf-8 -*-

from pipobot.lib.module_test import ModuleTest
from pipobot.lib.modules import SyncModule, defaultcmd

from .fact import fact

class CmdQuote(SyncModule):
    '''Retrieve a sentence from reverso.net, matching keywords and a language.

    Configuration keys:
        - lang: Define the default language used to retrieve the "quotes"/"facts".
        - size: Define the history size (the bot tries to doesn't repeat itself).
        - fall: Define the fallback keyword used when no history is available.'''
    _config = (("lang", str, "fr"), ("size", int, 256), ("fall", str, "fr"))

    def __init__(self, bot):
        desc = _('fact <txt> [-<lang>]: find a fact with <txt> in <lang> on reverso.net')
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name='fact')
        # config: lang, size, fall
        self.last = self.fall
        self.buff = []

    @defaultcmd
    def answer(self, sender, message):
        return fact(self, message)

class QuoteTest(ModuleTest):
    def test_fact(self):
        rep = self.bot_answer('!fact furet mort')
        self.assertEqual(rep[:77], 'De tout. Al Qaeda, les furets, les édulcorants artificiels, les distributeurs')
        rep = self.bot_answer('!fact furet')
        self.assertEqual(rep[:73], 'Des manipulations quotidiennes pendant ce stade critique du développement')
        rep = self.bot_answer('!fact chargé')
        self.assertEqual(rep[:71], u'Plus pr\xe9cis\xe9ment, le porteur charg\xe9 positivement est un polypeptide cha')
