#-*- coding: utf-8 -*-

import random
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from pipobot.lib.abstract_modules import FortuneModule
from pipobot.lib.module_test import ModuleTest


SITE = "http://secouchermoinsbete.fr"


class CmdScmb(FortuneModule):
    def __init__(self, bot):
        desc = """Pour appendre des choses grâce à secouchermoinsbete.fr
scmb : Retourne une information aléatoire.
scmb [n] : Affiche l'information [n]"""
        FortuneModule.__init__(self,
                               bot,
                               desc=desc,
                               name="scmb",
                               url_random="%s/random" % SITE,
                               url_indexed=SITE + "/%s-content",
                               lock_time=5,
                               )

    def extract_data(self, html_content):
        soup = BeautifulSoup(html_content)
        sections = soup.findAll("div", {"class": "anecdote-content-wrapper"})
        # If we are in a random page, we select a quote then continue parsing
        if sections != []:
            choice = sections[0]
            details = choice.findAll("p", {"class": "summary"})
            choiced = random.choice(details)
            url = "%s%s" % (SITE, choiced.a.get("href"))
            page = urllib.request.urlopen(url)
            content = page.read()
            page.close()
            soup = BeautifulSoup(content)

        article = soup.find("article", {"class": "anecdote"})
        if article is None:
            return "scmb invalide !!"
        quote = article.find("p", {"class": "summary"}).text
        nb = article.get("id").partition("-")[2]
        result = "scmb#%s : \n%s" % (nb, quote)
        return result.rstrip()


class ScmbTest(ModuleTest):
    def test_random(self):
        self.assertRegexpListMatches(self.bot_answer("!scmb"),
                                     ["scmb invalide !!", r"scmb#(\d+) : .*"])

    def test_fail(self):
        self.assertEqual(self.bot_answer("!scmb 42"), "http://secouchermoinsbete.fr/42-content n'existe pas !")

    def test_ok(self):
        self.assertRegexpMatches(self.bot_answer("!scmb 133"), r"scmb#(\d+) : .*")
