#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import urllib
from BeautifulSoup import BeautifulSoup
import threading

from pipobot.lib.modules import defaultcmd, answercmd
from pipobot.lib.abstract_modules import NotifyModule
from pipobot.lib.unittest import GroupUnitTest, ReTest, UnitTest, ExceptTest
import bandm_lib


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
                              command=u"b&m",
                              delay=10,
                              )
        self.old = ""
        self.mute = True

#######################################################################
#####################   Current-like operations   #####################
#######################################################################

    @answercmd("^$")
    def default(self, sender, message):
        current = bandm_lib.current()
        res = u"Titre en cours : %s" % (current)
        return res

    @answercmd("current")
    def current(self, sender, message):
        return self.default(sender, message)

#######################################################################
#####################   List operations ###############################
#######################################################################
    @answercmd("next")
    def list(self, sender, message):
        nb = 1 if message == "" else int(message)
        res = bandm_lib.get_next(nb)
        return res

    @answercmd("prev")
    def listprev(self, sender, message):
        nb = 1 if message == "" else int(message)
        res = bandm_lib.get_prev(nb)
        return res

    @answercmd("prog")
    def prog(self, sender, message):
        nb = 0 if message == "" else int(message)
        res = bandm_lib.get_shows(nb)
        return res

#######################################################################
#####################   Lyrics   ######################################
#######################################################################

    @answercmd("lyrics")
    def lyrics(self, sender, message):
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


class BandMTest(GroupUnitTest):
    def __init__(self, bot):
        tests = []
        tests.append(ReTest(cmd="!b&m",
                            expected="Titre en cours : (.*)"))
        tests.append(UnitTest(cmd="!b&m next 3",
                              tst_fct=lambda res: self.custom_test(res, 3)))
        tests.append(UnitTest(cmd="!b&m prev 3",
                              tst_fct=lambda res: self.custom_test(res, 3)))
        tests.append(ExceptTest(cmd="!b&m prog"))
        tests.append(ExceptTest(cmd="!b&m lyrics"))
        GroupUnitTest.__init__(self, tests, bot, "b&m")

    def custom_test(self, res, size):
        error = res.count("\n") != size - 1
        msg = ""
        if error:
            msg = "This test should return 3 lines of text !"
        return error, msg
