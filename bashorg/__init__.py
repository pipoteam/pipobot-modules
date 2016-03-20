# -*- coding: utf-8 -*-
""" A module to parse quotes from http://bash.org """

from BeautifulSoup import BeautifulSoup
from pipobot.lib.abstract_modules import FortuneModule
from pipobot.lib.module_test import ModuleTest
from pipobot.lib.utils import xhtml2text


class CmdBashorg(FortuneModule):
    """ Command !bashorg """

    def __init__(self, bot):
        desc = """To read quotes from bash.org
bashorg : Returns a random quote from bash.org.
bashorg [n] : Show the quote [n] from bash.org"""
        FortuneModule.__init__(self,
                               bot,
                               desc=desc,
                               name="bashorg",
                               url_random="http://bash.org/?random",
                               url_indexed='http://bash.org/?%s',
                               lock_time=2,
                               )

    def extract_data(self, html_content):
        """ Extracts a bashorg quote given the HTML code of the page """
        soup = BeautifulSoup(html_content)
        sections = soup.findAll("p", {"class": "qt"})
        if sections == []:
            return "The quote does not exist !"

        tables = soup.findAll("table")
        for elt in tables:
            p = elt.findAll("p", {"class": "qt"})
            if p != []:
                content = xhtml2text(unicode(p[0]))
                nb = xhtml2text(unicode(elt.findAll("b")[0].text))
                break

        return "bashorg %s :\n%s" % (nb, content)


class BashfOrgTest(ModuleTest):
    def test_bashorg_ok(self):
        bot_rep = self.bot_answer("!bashorg 1729")
        expected = (u"bashorg #1729 :\n"
                    u"<blinkchik> can i become a bot and how??")
        self.assertEqual(bot_rep, expected)

    def test_bashorg_random(self):
        bot_rep = self.bot_answer("!bashorg")
        expected_re = [r"bashorg #(\d+) :(.*)",
                       r"The quote does not exist !"]
        self.assertRegexpListMatches(bot_rep, expected_re)

    def test_bashorg_404(self):
        bot_rep = self.bot_answer("!bashorg 42")
        expected = "The quote does not exist !"
        self.assertEqual(bot_rep, expected)
