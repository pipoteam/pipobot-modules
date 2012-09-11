#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import logging
import threading
import string
import ast
import operator as op
from pipobot.lib.modules import SyncModule, answercmd
from pipobot.lib.unittest import UnitTest
from lettres import Lettres
from chiffres import Chiffres, CalcError

logger = logging.getLogger("pipobot.chiffres_lettres")


class ChiffresCmd(SyncModule):
    def __init__(self, bot):
        desc = u"Le module du jeux des chiffres et des lettres\n"
        desc += u"chiffres init : génère une nouvelle partie\n"
        desc += u"chiffres solve : cherche à résoudre le problème"
        self.game = None
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            command="chiffres")

        # Activated printers and their names
        self.printers = { 'br': ChiffresCmd.pretty_br, 'lisp': ChiffresCmd.pretty_lisp, 'tiles': ChiffresCmd.pretty_tiles }
        self.default_printer = 'tiles'

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

        printer = self.printers[self.default_printer]
        if args and self.printers.get(args) :
            printer = self.printers[args]

        self.timer.cancel()

        if exact:
            return u"J'ai trouvé une solution exacte : \n%s" % printer(res.ast, exact)
        else:
            return u"Pas de solution exacte… voici ce que j'ai de mieux : \n%s" % printer(res.ast, exact)

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

    #
    # Some printers for ast describing a solve
    #

    opstr = {ast.Add: u'+', ast.Sub: u'-', ast.Mult: u'×', ast.Div: u'÷'}
    opast = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.div}

    @staticmethod
    def pretty_lisp(astree, exact) :
        """ Print ast tree in algebra formula. Its name is a reference to the number of parentheses that it involves """

        if isinstance(astree, ast.Num) :
            return unicode(astree.n)
        elif isinstance(astree, ast.BinOp) :
            return u'(%s%s%s)' % (ChiffresCmd.pretty_lisp(astree.left, exact),
                                  ChiffresCmd.opstr[astree.op],
                                  ChiffresCmd.pretty_lisp(astree.right, exact))


    @staticmethod
    def pretty_br(astree, exact) :
        """ A pretty printer imitating the fantastic Betrand Renard """

        def inside(astree) :
            if isinstance(astree.left, ast.Num) and isinstance(astree.right, ast.Num) :
                res = ChiffresCmd.opast[astree.op](astree.left.n, astree.right.n)
                return (u"Avec les nombres de départs, vous voyez on a %d %s %d, ce qui donne %d\n" % \
                        (astree.left.n, ChiffresCmd.opstr[astree.op], astree.right.n, res),
                        res)
            elif isinstance(astree.left, ast.Num) :
                before, bres = inside(astree.right)
                res = ChiffresCmd.opast[astree.op](astree.left.n, bres)
                return (before + \
                        u"Et après ? Et ben on prend le %d calculé et le %d du tirage, un coup de %s et hop, %d\n" % \
                                    (bres, astree.left.n, ChiffresCmd.opstr[astree.op], res),
                        res)
            elif isinstance(astree.right, ast.Num) :
                before, bres = inside(astree.left)
                res = ChiffresCmd.opast[astree.op](bres, astree.right.n)
                return (before + \
                        u"Vous vous croyez coincé ? Et non, le %d %s le %d du tirage, ça donne %d\n" % \
                                    (bres, ChiffresCmd.opstr[astree.op], astree.right.n, res),
                        res)
            else :
                beforel, bresl = inside(astree.left)
                beforer, bresr = inside(astree.right)
                res = ChiffresCmd.opast[astree.op](bresl, bresr)
                return  (beforel +\
                         beforer +\
                         u"On prend le %d et le %d, on fait %s et on arrive à %d\n" %
                                    (bresl, bresr, ChiffresCmd.opstr[astree.op], res),
                         res)

        mess, res = inside(astree)
        if exact:
            mess += u"Et voila, on arrive bien à %d, c'était pas compliqué" % res
        else:
            mess += u"Bon ben, j'ai fait ce que j'ai pu et j'arrive à %d" % res
        return mess

    @staticmethod
    def pretty_tiles(astree, exact) :
        """ A pretty printer showing the results as with the tiles """

        def inside(astree) :
            if isinstance(astree.left, ast.Num) and isinstance(astree.right, ast.Num) :
                res = ChiffresCmd.opast[astree.op](astree.left.n, astree.right.n)
                return (u"%d %s %d = %d\n" % \
                        (astree.left.n, ChiffresCmd.opstr[astree.op], astree.right.n, res),
                        res)
            elif isinstance(astree.left, ast.Num) :
                before, bres = inside(astree.right)
                res = ChiffresCmd.opast[astree.op](astree.left.n, bres)
                return (before + \
                        u"%d %s %d = %d\n" % \
                        (bres, ChiffresCmd.opstr[astree.op], astree.left.n, res),
                        res)
            elif isinstance(astree.right, ast.Num) :
                before, bres = inside(astree.left)
                res = ChiffresCmd.opast[astree.op](bres, astree.right.n)
                return (before + \
                        u"%d %s %d = %d\n" % \
                        (bres, ChiffresCmd.opstr[astree.op], astree.right.n, res),
                        res)
            else :
                beforel, bresl = inside(astree.left)
                beforer, bresr = inside(astree.right)
                res = ChiffresCmd.opast[astree.op](bresl, bresr)
                return  (beforel +\
                         beforer +\
                         u"%d %s %d = %d\n" % \
                                    (bresl, ChiffresCmd.opstr[astree.op], bresr, res),
                         res)

        return inside(astree)[0].strip()


class LettresCmd(SyncModule):
    _config = (("dico", str, ""),)

    def __init__(self, bot):
        desc = u"Le module du jeux des chiffres et des lettres\n"
        desc += u"lettres init : génère une nouvelle partie\n"
        desc += u"lettres solve : cherche à résoudre le problème"

        if self.dico == "":
            logger.error(_("Missing dictionary for lettres modules. "
                           "Solving function will not work !"))

        self.game = Lettres(self.dico)
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
        if results is None:
            return u"Je n'ai pas de dictionnaire dans ma config :'("

        self.game.letters = []
        return u"Voici ce que j'ai trouvé : \n%s" % ", ".join(results)

    def time_out(self):
        self.bot.say(u"Temps écoulé !! On arrête de chercher !")


class ChiffresTest(UnitTest):
    def __init__(self, bot):
        cmd = (("!chiffres init", {"type": UnitTest.RE,
                                   "expected": u"Nouvelle partie lancée\nTotal à trouver : (\d+)\n"
                                               u"Nombres fournis : [(\d+),]*(\d+)",
                                   "desc": "Test de !chiffres init"}),
               ("!chiffres solve", {"type": UnitTest.RE,
                                    "expected": [u"J'ai trouvé une solution exacte(.*)",
                                                 u"Pas de solution exacte…(.*)"],
                                    "desc": "Test !chiffres solve"}),
               )
        UnitTest.__init__(self, cmd, bot, "chiffres")
