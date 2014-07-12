#-*- coding: utf-8 -*-
""" A module to parse quotes from http://bash.org """

from bs4 import BeautifulSoup

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
        quote = soup.find("p", {"class": "quote"})
        if quote is None:
            return "The quote does not exist !"

        quote_id = quote.find("a").text
        quote = soup.find("p", {"class": "qt"})

        return "bashorg %s :\n%s" % (quote_id, xhtml2text(str(quote)))


class BashfOrgTest(ModuleTest):
    def test_bashorg_ok(self):
        """ !bashorg 1729 """
        bot_rep = self.bot_answer("!bashorg 1729")
        expected = ("bashorg #1729 :\n"
                    "<blinkchik> can i become a bot and how??")
        self.assertEqual(bot_rep, expected)

    def test_bashorg_random(self):
        """ !bashorg """
        bot_rep = self.bot_answer("!bashorg")
        expected_re = [r"bashorg #(\d+) :(.*)",
                       r"The quote does not exist !"]
        self.assertRegexpListMatches(bot_rep, expected_re)

    def test_bashorg_404(self):
        """ !bashorg 42 """
        bot_rep = self.bot_answer("!bashorg 42")
        expected = "The quote does not exist !"
        self.assertEqual(bot_rep, expected)
