#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
import urllib.request

from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.utils import xhtml2text


URL = "http://www.chucknorrisfacts.fr/api/get?data=nb:1;type:txt;tri:alea"

class CmdChuck(SyncModule):
    def __init__(self, bot):
        desc = """Pour afficher des chucknorrisfact.
chuck : Retourne un fact aléatoire.
chuck [n] : Affiche le fact [n]"""
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="chuck",
                            lock_time=2,
                           )

    @defaultcmd
    def answer(self, sender, message):
        page = urllib.request.urlopen(URL)
        content = page.read()

        ret = json.loads(content.decode("utf-8"))[0]
        return "Fact #%s : %s" % (ret["id"], xhtml2text(ret["fact"]))
