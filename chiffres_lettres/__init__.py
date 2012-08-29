#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import threading
import string
from pipobot.lib.modules import SyncModule, answercmd
from lettres import Lettres
from chiffres import Chiffres, CalcError


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
        if hasattr(self, "timer"):
            self.timer.cancel()

        self.timer = threading.Timer(60, self.time_out)
        self.timer.start()
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

    @answercmd("check")
    def check(self, sender, args):
        if self.game is None:
            return u"Aucune partie lancée"

        try:
            verdict = self.game.check(args)
            if verdict:
                if verdict == self.game.total:
                    return u"%s : Le compte est bon !!" % sender
                    self.timer.cancel()
                else:
                    return u"%s : Les calculs sont bons, tu trouves %s au lieu de %s, soit une erreur de %s" % (sender, 
                                                                                    verdict,
                                                                                    self.game.total,
                                                                                    abs(verdict - self.game.total))
            else:
                return u"%s : Désolé mais tu ne sais pas compter" % sender

        except CalcError as err:
            return u"%s: %s" % (sender, err)

    def time_out(self):
        self.bot.say("Temps écoulé !! On arrête de compter !")


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
        t = threading.Timer(60, self.time_out)
        t.start()
        return res
    
    @answercmd("solve")
    def solve(self, sender, args):
        if self.game.letters == []:
            return u"Aucune partie lancée"

        results = self.game.solve()
        self.game.letters = []
        return u"Voici ce que j'ai trouvé : \n%s" % ", ".join(results)

    def time_out(self):
        self.bot.say(u"Temps écoulé !! On arrête de chercher !")
