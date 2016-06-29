# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from pipobot.lib.abstract_modules import FortuneModule
from pipobot.lib.utils import xhtml2text


class CmdMultideskOS(FortuneModule):
    """A module to parse multideskos quotes"""

    def __init__(self, bot):
        desc = u"Pour lire des quotes multideskos\n"
        desc += u"multideskos : Retourne une quote aléatoire de multideskos."
        FortuneModule.__init__(self,
                               bot,
                               desc=desc,
                               name="multideskos",
                               url_random="http://www.multideskos.com/",
                               url_indexed='http://www.multideskos.com/%s.html',
                               lock_time=2,
                               )

    def extract_data(self, html_content):
        soup = BeautifulSoup(html_content)
        quote = soup.findAll('div', {"class":'citation'})[0]
        return xhtml2text('\n'.join([p.contents[0] for p in quote.contents]))
