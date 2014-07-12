#-*- coding: utf-8 -*-
""" A module to parse quote extracted from http://danstonchat.com/ """

import re
import random
from pipobot.lib.utils import xhtml2text
from bs4 import BeautifulSoup
from pipobot.lib.abstract_modules import FortuneModule
from pipobot.lib.module_test import ModuleTest


class CmdBashfr(FortuneModule):
    """A module to parse bashfr quotes"""

    def __init__(self, bot):
        desc = """Pour lire des quotes bashfr
bashfr : Retourne une quote aléatoire de bashfr.
bashfr [n] : Affiche la quote [n] de bashfr"""
        FortuneModule.__init__(self,
                               bot,
                               desc=desc,
                               name="bashfr",
                               url_random="http://danstonchat.com/random.html",
                               url_indexed='http://danstonchat.com/%s.html',
                               lock_time=2,
                              )

    def extract_data(self, html_content):
        """Extracts the content of the quote given
           the HTML code of a bashfr page"""
        soup = BeautifulSoup(html_content)
        sections = soup.findAll("p", {"class": "item-content"})
        choiced = random.choice(sections)
        contents = choiced.a.contents
        quote_url = choiced.a["href"]
        quote_id = re.match(r"http://danstonchat.com/(\d+).html",
                            quote_url).group(1)

        result = ""
        for i in contents:
            result += xhtml2text(str(i))

        return "bashfr #%s :\n%s" % (quote_id, result)


class BashfrTest(ModuleTest):
    def test_bashfr_5(self):
        """ !bashfr 5 """
        bot_rep = self.bot_answer("!bashfr 5")
        expected = ("bashfr #5 :\n"
                    "(swatchtim) mac ? ca existe encore ca ?\n"
                    " * kick: (swatchtim) was kicked by (Cafmac) (Ouais. Les cons aussi.)")
        self.assertEqual(bot_rep, expected)

    def test_bashfr_random(self):
        """ !bashfr """
        bot_rep = self.bot_answer("!bashfr")
        expected_re = [r"bashfr #(\d+) :(.*)",
                       r"La quote demandée n'existe pas.(.*)"]
        self.assertRegexpListMatches(bot_rep, expected_re)

    def test_bashfr_404(self):
        """ !bashfr 42 """
        bot_rep = self.bot_answer("!bashfr 42")
        expected = "http://danstonchat.com/42.html n'existe pas !"
        self.assertEqual(bot_rep, expected)
