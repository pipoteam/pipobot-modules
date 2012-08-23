#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import string
from pipobot.lib.modules import SyncModule, answercmd
from lettres import Lettres


class ChiffresCmd(SyncModule):
    def __init__(self, bot):
        desc = u"Le module du jeux des chiffres et des lettres\n"
        desc += u"chiffres init : génère une nouvelle partie\n"
        desc += u"chiffres solve : cherche à résoudre le problème"
        self.game = None
        SyncModule.__init__(self,
                            bot, 
                            desc = desc,
                            command = "chiffres")

    @answercmd("init")
    def init(self, sender, args):
        self.game = Chiffres()
        res = u"Nouvelle partie lancée\n"
        res += u"Total à trouver : %s\n" % self.game.total
        res += u"Nombres fournis : %s" % ', '.join(map(str, self.game.digits))
        return res
    
    @answercmd("solve")
    def solve(self, sender, args):
        if self.game is None:
            return u"Aucune partie lancée"
        exact, res = self.game.solve()
        if exact:
            return u"J'ai trouvé une solution exacte : \n%s" % res
        else:
            return u"Pas de solution exacte… voici ce que j'ai de mieux : \n%s" % res
        

class LettresCmd(SyncModule):
    def __init__(self, bot):
        desc = u"Le module du jeux des chiffres et des lettres\n"
        desc += u"lettres init : génère une nouvelle partie\n"
        desc += u"lettres solve : cherche à résoudre le problème"
        self.game = Lettres()
        SyncModule.__init__(self,
                            bot, 
                            desc = desc,
                            command = "lettres")

    @answercmd("init")
    def init(self, sender, args):
        self.game.tirage()
        res = u"Nouvelle partie lancée\n"
        res += u"Liste des lettres fournies : %s" % ", ".join(self.game.letters)
        return res
    
    @answercmd("solve")
    def solve(self, sender, args):
        if self.game.letters == []:
            return u"Aucune partie lancée"

        results = self.game.solve()
        self.game.letters = []
        return u"Voici ce que j'ai trouvé : \n%s" % ", ".join(results)
