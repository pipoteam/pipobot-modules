#-*- coding: utf-8 -*-

import urllib.request, urllib.parse, urllib.error
import re
from bs4 import BeautifulSoup
from pipobot.lib.modules import SyncModule, defaultcmd


class CmdSosBides(SyncModule):
    def __init__(self, bot):
        desc = "sos_bides : Fait appel à une superbe blague pour passer inaperçu"
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="sos_bides")

    @defaultcmd
    def answer(self, sender, message):
        url = urllib.request.urlopen("http://www.blablagues.net/hasard.html")
        soup = BeautifulSoup(url.read())
        html = soup.find("div", {"class": "blague"}).findAll("div")
        res = ""
        for div in html:
            res += "\n" + div.renderContents().decode("utf-8")
        res = re.sub("<br />\r\n", "\n", res)
        res = re.sub("<[^>]*>", "", res)
        return res.strip()

