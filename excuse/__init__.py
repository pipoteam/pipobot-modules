# -*- coding: utf-8 -*-

import pipobot.lib.utils
from BeautifulSoup import BeautifulSoup
from pipobot.lib.abstract_modules import FortuneModule


class CmdExcuse(FortuneModule):
    def __init__(self, bot):
        desc = """Pour afficher des excuse aléatoires.
excuse : Retourne une excuse."""
        FortuneModule.__init__(self,
                               bot,
                               desc=desc,
                               name="excuse",
                               url_random="http://programmingexcuses.com/",
                               url_indexed="http://programmingexcuses.com/",
                               lock_time=2,
                               )

    def extract_data(self, html_content):
        soup = BeautifulSoup(html_content)
        div = soup.find("div", {"class": "wrapper"})
        excuse = div.find("center").find("a").text
        content = pipobot.lib.utils.xhtml2text(excuse)
        return content
