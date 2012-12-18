# -*- coding: utf-8 -*-

import urllib
import threading
import bandm_lib
from BeautifulSoup import BeautifulSoup
from pipobot.lib.modules import defaultcmd, answercmd
from pipobot.lib.abstract_modules import NotifyModule
from pipobot.lib.module_test import ModuleTest


class CmdBideEtMusique(NotifyModule):
    def __init__(self, bot):
        desc = {"": u"Pour afficher des infos sur bides et musique.",
                "current": u"Ce qui passe actuellement sur bides et musique",
                "next [n]": u"Les [n] chansons à venir (dans la limite des stocks disponibles)",
                "prev [n]": u"Les [n] chansons précédentes (dans la limite des stocks disponibles)",
                "prog [n]": u"Les programmes de la journée J+n",
                "mute": u"N'affiche plus les nouvelles chansons.",
                "unmute": u"Affiche les nouvelles chansons.",
                "lyrics": u"Les paroles de la chanson courante",
                }
        NotifyModule.__init__(self,
                              bot,
                              desc=desc,
                              name=u"b&m",
                              delay=10,
                              )
        self.old = ""

#######################################################################
#####################   Current-like operations   #####################
#######################################################################

    @answercmd("", "current")
    def default(self, sender):
        current = bandm_lib.current()
        res = u"Titre en cours : %s" % (current)
        return res

#######################################################################
#####################   List operations ###############################
#######################################################################
    @answercmd("next", "next (?P<n>\d+)")
    def list(self, sender, n=1):
        res = bandm_lib.get_next(int(n))
        return res

    @answercmd("prev", "prev (?P<n>\d+)")
    def listprev(self, sender, n=1):
        res = bandm_lib.get_prev(int((n)))
        return res

    @answercmd("prog", "prog (?P<n>\d+)")
    def prog(self, sender, n=0):
        res = bandm_lib.get_shows(int(n))
        return res

#######################################################################
#####################   Lyrics   ######################################
#######################################################################

    @answercmd("lyrics")
    def lyrics(self, sender):
        return bandm_lib.lyrics()

#######################################################################
#####################   Notifications   ###############################
#######################################################################

    def do_action(self):
        new = bandm_lib.current()
        if new != self.old:
            self.bot.say(u"Nouvelle chanson : %s" % new)
            self.old = new

    def update(self, silent=False):
        self.old = bandm_lib.current()


class BandMTest(ModuleTest):
    def test_current(self):
        bot_rep = self.bot_answer("!b&m")
        self.assertRegexpMatches(bot_rep, "Titre en cours : (.*)")

    def test_lyrics(self):
        self.bot_answer("!b&m lyrics")

    def test_next_3(self):
        nb = 3
        bot_rep = self.bot_answer("!b&m next %s" % nb)
        self.assertEqual(bot_rep.count("\n"),
                         nb - 1,
                         msg="Result %s should be a %s-line string" % (bot_rep, nb))

    def test_prev_3(self):
        nb = 3
        bot_rep = self.bot_answer("!b&m prev %s" % nb)
        self.assertEqual(bot_rep.count("\n"),
                         nb - 1,
                         msg="Result %s should be a %s-line string" % (bot_rep, nb))

    def test_prog(self):
        self.bot_answer("!b&m prog")
