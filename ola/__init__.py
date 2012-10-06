#! /usr/bin/env python
#-*- coding: utf-8 -*-
import random
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.module_test import ModuleTest

FAIL_MSG = u"On veut un entier quand même…"
OLA = ["\o/ .o. .o. .o.", ".o. \o/ .o. .o.",
       ".o. .o. \o/ .o.", ".o. .o. .o. \o/"]
OLA_REV = list(OLA)
OLA_REV.reverse()

class Ola(SyncModule):
    def __init__(self, bot):
        SyncModule.__init__(self,
                            bot,
                            desc="Fait la ola.",
                            command="ola")

    @defaultcmd
    def answer(self, sender, message):
        if message == "":
            message = str(random.randint(0, 1))
        if not message.isdigit():
            return FAIL_MSG
        return OLA if int(message) % 2 == 0 else OLA_REV


class TestOla(ModuleTest):
    def test_ola_fail(self):
        rep = self.bot_answer("!ola qsdf")
        self.assertEqual(rep, FAIL_MSG)

    def test_ola_int(self):
        rep = self.bot_answer("!ola 5")
        self.assertEqual(rep, "\n".join(OLA_REV))

    def test_ola_random(self):
        rep = self.bot_answer("!ola")
        self.assertIn(rep, ["\n".join(OLA), "\n".join(OLA_REV)])
