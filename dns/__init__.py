#-*- coding: utf-8 -*-

import socket
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.module_test import ModuleTest


class CmdDns(SyncModule):
    def __init__(self, bot):
        desc = _("dns <host>: Prints the IP of <host>")
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="dns")

    @defaultcmd
    def answer(self, sender, message):
        return socket.gethostbyname(message)


class DnsTest(ModuleTest):
    def test_dns(self):
        self.assertRegexpMatches(self.bot_answer("!dns bde.enseeiht.fr"), u"147.127.161.150")
