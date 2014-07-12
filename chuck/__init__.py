#-*- coding: utf-8 -*-

import requests

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
        req = requests.get(URL)
        if req.status_code == 200:
            ret = req.json()[0]
            return "Fact #%s : %s" % (ret["id"], xhtml2text(ret["fact"]))
        else:
            return "HTTP Error %d on module chuck" % req.status_code
