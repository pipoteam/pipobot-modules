#-*- coding: utf-8 -*-

import pipobot.lib.utils
from BeautifulSoup import BeautifulSoup
from pipobot.lib.abstract_modules import FortuneModule
from pipobot.lib.module_test import ModuleTest


ERROR_MSG = (u"Je n'arrive pas à parser la page : peut-être que l'html a changé, "
             u"ou la page cherchée n'existe pas, ou alors mon développeur est un boulet")



class CmdVdm(FortuneModule):
    def __init__(self, bot):
        desc = """Pour afficher des vdm.
vdm : Retourne une vdm aléatoire.
vdm [n] : Affiche la vdm [n]"""
        FortuneModule.__init__(self,
                               bot,
                               desc=desc,
                               name="vdm",
                               url_random="http://www.viedemerde.fr/aleatoire",
                               url_indexed="http://www.viedemerde.fr/travail/%s",
                               lock_time=2,
                               )

    def extract_data(self, html_content):
        soup = BeautifulSoup(html_content)
        res = []
        try:
            a = soup.find("div", {"class": "post article"}).find("p")
            for elt in a.findAll("a"):
                res.append(pipobot.lib.utils.xhtml2text(elt.text))
            nb = a.findAll("a")[0].get("href").split("/")[-1]
            res = (u"VDM#%s : %s" % (nb, "".join(res))).replace(".", ". ")
        except:
            res = ERROR_MSG
        return res


class VdmTest(ModuleTest):
    def test_random(self):
        self.assertRegexpListMatches(self.bot_answer("!vdm"),
                                     [ERROR_MSG, r"VDM#(\d+) : .*"])

    def test_fail(self):
        self.assertEqual(self.bot_answer("!vdm 442"),
                         ERROR_MSG)

    def test_ok(self):
        self.assertRegexpMatches(self.bot_answer("!vdm 45980"),
                                 r"VDM#(\d+) : .*")
