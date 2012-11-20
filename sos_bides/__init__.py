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
                            command="sos_bides")

    @defaultcmd
    def answer(self, sender, message):
        url = urllib.urlopen("http://www.blaguemarrante.com/Blague")
        soup = BeautifulSoup(url.read())
        html = soup.findAll('p')[1].prettify()
        html = re.sub('<[^>]*p>', '', html)
        html = re.sub('<br />', '\n', html)
        html = re.sub('(\n)+', '\n', html)
        joke = html.split("<a")[0]
        return xhtml2text(joke.strip())

