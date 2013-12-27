#-*- coding: utf-8 -*-

import json
import urllib.request, urllib.parse, urllib.error
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.module_test import ModuleTest
from pipobot.lib.utils import xhtml2text

NOT_FOUND = "Rien de trouvé :'("


class CmdWiki(SyncModule):
    def __init__(self, bot):
        desc = "wiki word : Cherche la définition d'un mot dans le wikitionary"
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="wiki")

    @defaultcmd
    def answer(self, sender, message):
        url = "http://fr.wiktionary.org/w/api.php?action=query&list=search&format=json&srsearch=%s&srlimit=10" % message
        page = urllib.request.urlopen(url)
        content = page.read()
        page.close()
        js = json.loads(content.decode("utf-8"))
        try:
            snippet = xhtml2text(js["query"]["search"][0]["snippet"])
            #Removing prononciation
            splitted = snippet
            clean = snippet.replace("  ", " ")
            return clean if clean != "" else NOT_FOUND
        except (KeyError, IndexError):
            return NOT_FOUND


class TestWiki(ModuleTest):
    def test_ok(self):
        rep = self.bot_answer("!wiki pipo")
        self.assertIn("pipo", rep)

    def test_ko(self):
        rep = self.bot_answer("!wiki pipoteam")
        self.assertEqual(rep, "Rien de trouvé :'(")
