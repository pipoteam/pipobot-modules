#-*- coding: utf-8 -*-
""" A module to parse quote extracted from http://danstonchat.com/ """

import random
import pipobot.lib.utils
from BeautifulSoup import BeautifulSoup
from pipobot.lib.abstract_modules import FortuneModule
from pipobot.lib.unittest import UnitTest


class CmdBashfr(FortuneModule):
    """A module to parse bashfr quotes"""
    def __init__(self, bot):
        desc = """Pour lire des quotes bashfr
bashfr : Retourne une quote aléatoire de bashfr.
bashfr [n] : Affiche la quote [n] de bashfr"""
        FortuneModule.__init__(self,
                               bot,
                               desc=desc,
                               command="bashfr",
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
            result = u""
            for i in tableau:
                if unicode(i) == u"<br />":
                    result += "\n"
                else:
                    result = result + pipobot.lib.utils.xhtml2text(unicode(i))
            return "bashfr #%s :\n%s" % (quote_id, result)


class BashfrTest(UnitTest):
    def __init__(self, bot):
        cmd = (("!bashfr", {"type" : UnitTest.RE,
                            "expected" : ["bashfr #(\d+) :(.*)", "La quote demandée n'existe pas.(.*)"],
                            "sender" : "test",
                            "desc" : "Test random bashfr"}),
                ("!bashfr 42", {"type" : UnitTest.EXACT,
                                "expected" : "La quote demandée n'existe pas. (Erreur 404)",
                                "sender" : "test",
                                "desc" : "Test erreur 404 sur bashfr"}),
                ("!bashfr 5", {"type" : UnitTest.EXACT,
                               "expected" : ("bashfr #5 :\n"
                                             "(swatchtim) mac ? ca existe encore ca ?\n"
                                             " * kick: (swatchtim) was kicked by (Cafmac) (Ouais. Les cons aussi.)"),
                                "sender" : "test",
                                "desc" : "Test OK sur bashfr"}))
        UnitTest.__init__(self, cmd, bot, "bashfr")
