#! /usr/bin/env python
#-*- coding: utf-8 -*-

import time
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.unittest import UnitTest


class CmdDate(SyncModule):
    def __init__(self, bot):
        desc = "date : Affiche la date et l'heure actuelle"
        SyncModule.__init__(self, 
                            bot,  
                            desc = desc,
                            command = "date")

    @defaultcmd    
    def answer(self, sender, message):
        return time.strftime("Nous sommes le %d/%m/%Y et il est %H:%M")


class DateTest(UnitTest):
    def __init__(self, bot):
        cmd = (("!date", {"type": UnitTest.RE,
                          "expected": u"Nous sommes le (\d+)/(\d+)/(\d+) et il est (\d+):(\d+)",
                          "desc": "Test de !date"}),
               )
        UnitTest.__init__(self, cmd, bot, "date")
