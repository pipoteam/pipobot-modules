#! /usr/bin/env python
#-*- coding: utf-8 -*-

import json
import urllib
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.utils import xhtml2text

class CmdWiki(SyncModule):
    def __init__(self, bot):
        desc = "wiki word : Cherche la définition d'un mot dans le wikitionary"
        SyncModule.__init__(self,
                            bot,
                            desc = desc,
                            command = "wiki")

    @defaultcmd
    def answer(self, sender, message):
        url = "http://fr.wiktionary.org/w/api.php?action=query&list=search&format=json&srsearch=%s&srlimit=10" % message
        page = urllib.urlopen(url)
        content = page.read()
        page.close()
        js = json.loads(content)
        try:
            snippet = xhtml2text(js["query"]["search"][0]["snippet"])
            #Removing prononciation
            splitted = snippet
            return snippet.replace("  ", " ")
        except KeyError, IndexError:
            return u"Rien de trouvé :'("
