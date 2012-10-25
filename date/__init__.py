#-*- coding: utf-8 -*-

import time
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.module_test import ModuleTest



class CmdDate(SyncModule):
    def __init__(self, bot):
        desc = "date : Affiche la date et l'heure actuelle"
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            command="date")

    @defaultcmd
    def answer(self, sender, message):
        return time.strftime("Nous sommes le %d/%m/%Y et il est %H:%M")


class DateTest(ModuleTest):
    def test_date(self):
        expected = u"Nous sommes le (\d+)/(\d+)/(\d+) et il est (\d+):(\d+)"
        self.assertRegexpMatches(self.bot_answer("!date"), expected)
