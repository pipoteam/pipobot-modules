#! /usr/bin/env python
#-*- coding: utf-8 -*-

import pipobot.lib.utils
from BeautifulSoup import BeautifulSoup
from pipobot.lib.abstract_modules import FortuneModule
from pipobot.lib.unittest import GroupUnitTest, ReTest, ExactTest

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
                               command="vdm",
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


class VdmTest(GroupUnitTest):
    def __init__(self, bot):
        tests = []
        tests.append(ReTest(cmd="!vdm",
                            expected=[ERROR_MSG, r"VDM#(\d+) : .*"],
                            desc="Test vdm random"))
        tests.append(ExactTest(cmd="!vdm 442",
                               expected=ERROR_MSG,
                               desc="Erreur vdm"))
        tests.append(ReTest(cmd="!vdm 45980",
                            expected=r"VDM#(\d+) : .*",
                            desc="Test fonctionnement correct vdm"))
        GroupUnitTest.__init__(self, tests, bot, "vdm")
