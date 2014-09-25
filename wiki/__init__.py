#-*- coding: utf-8 -*-

import requests
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
        params = {"action": "query",
                  "list": "search",
                  "format": "json",
                  "srsearch": message,
                  "limit": "10"}
        ret = requests.get("http://fr.wiktionary.org/w/api.php", params=params)
        js = ret.json()
        try:
            snippet = xhtml2text(js["query"]["search"][0]["snippet"])
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
