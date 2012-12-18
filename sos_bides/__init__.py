#-*- coding: utf-8 -*-

import urllib
import re
from BeautifulSoup import BeautifulSoup
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.utils import xhtml2text


class CmdSosBides(SyncModule):
    def __init__(self, bot):
        desc = "sos_bides : Fait appel à une superbe blague pour passer inaperçu"
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="sos_bides")

    @defaultcmd
    def answer(self, sender, message):
        url = urllib.urlopen("http://www.blablagues.net/hasard.html")
        soup = BeautifulSoup(url.read())
        html = soup.find("div", {"class": "blague"}).findAll("div")
        res = u""
        for div in html:
            res += u"\n" + div.renderContents()
        res = re.sub(u"<br />\r\n", u"\n", res)
        res = re.sub(u"<[^>]*>", "", res)
        return res.strip()

