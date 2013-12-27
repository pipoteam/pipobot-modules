#-*- coding: utf-8 -*-
""" A module to parse quote extracted from http://danstonchat.com/ """

import random
import pipobot.lib.utils
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
        if soup.find("h2", text="Erreur 404"):
            return "La quote demandée n'existe pas. (Erreur 404)"
        else:
            sections = soup.findAll("p", {"class": "item-content"})
            choiced = random.randrange(len(sections))
            tableau = sections[choiced].a.contents
            quote_url = sections[choiced].a["href"]
            quote_id = quote_url.partition("/")[2].partition(".")[0]
            result = ""
            for i in tableau:
                if i == "<br />":
                    result += "\n"
                else:
                    result = result + pipobot.lib.utils.xhtml2text(str(i))
            return "bashfr #%s :\n%s" % (quote_id, result)


class BashfrTest(ModuleTest):
    def test_bashfr_5(self):
        bot_rep = self.bot_answer("!bashfr 5")
        expected=("bashfr #5 :\n"
                  "(swatchtim) mac ? ca existe encore ca ?\n"
                  " * kick: (swatchtim) was kicked by (Cafmac) (Ouais. Les cons aussi.)")
        self.assertEqual(bot_rep, expected)

    def test_bashfr_random(self):
        bot_rep = self.bot_answer("!bashfr")
        expected_re = [r"bashfr #(\d+) :(.*)",
                       r"La quote demandée n'existe pas.(.*)"]
        self.assertRegexpListMatches(bot_rep, expected_re)

    def test_bashfr_404(self):
        bot_rep = self.bot_answer("!bashfr 42")
        expected = "La quote demandée n'existe pas. (Erreur 404)"
        self.assertEqual(bot_rep, expected)
