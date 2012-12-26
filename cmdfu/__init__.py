#! /usr/bin/env python
#-*- coding: utf-8 -*-
import urllib
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.module_test import ModuleTest


class CmdCmdFu(SyncModule):
    def __init__(self, bot):
        desc = """Commandline tips
cmdfu : Retourne une commande aléatoire"""
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            command="cmdfu",
                            )

    @defaultcmd
    def answer(self, sender, message):
        url = "http://www.commandlinefu.com/commands/random/plaintext"
        url = urllib.urlopen(url)
        contenu = url.read()
        return "\n".join(contenu.strip().split("\n")[2:])


class TestCmdfu(ModuleTest):
    def test_cmdfu(self):
        self.assertNotEqual(self.bot_answer("!cmdfu"), "")
