#-*- coding: utf-8 -*-
import random
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.module_test import ModuleTest


class CmdPioche(SyncModule):
    def __init__(self, bot):
        desc = "pioche\nPioche une carte au hasard dans un jeu de 52 cartes"
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            command="pioche")

    @defaultcmd
    def answer(self, sender, message):
        n = random.randint(0, 51)
        couleurs = ["pique", "coeur", "carreau", "trèfle"]
        noms = [str(i) for i in range(2, 11)] + ["Valet", "Dame", "Roi", "As"]
        return noms[n % 13] + " de " + couleurs[n / 13]


class TestPioche(ModuleTest):
    def test_pioche(self):
        rep = self.bot_answer("!pioche")
        self.assertRegexpMatches(rep, "\S+ de (pique|coeur|trèfle|carreau)")
