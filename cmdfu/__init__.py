#-*- coding: utf-8 -*-
import requests
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.module_test import ModuleTest


class CmdCmdFu(SyncModule):
    def __init__(self, bot):
        desc = """Commandline tips
cmdfu : Retourne une commande aléatoire"""
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="cmdfu",
                           )

    @defaultcmd
    def answer(self, sender, message):
        url = "http://www.commandlinefu.com/commands/random/plaintext"
        req = requests.get(url)
        if req.status_code == 200:
            content = req.content.decode("utf-8")
            return "\n".join(content.strip().split("\n")[2:])
        else:
            return "HTTP Error %d on module cmdfu" % req.status_code


class TestCmdfu(ModuleTest):
    def test_cmdfu(self):
        self.assertNotEqual(self.bot_answer("!cmdfu"), "")
