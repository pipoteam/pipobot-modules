#! /usr/bin/env python
#-*- coding: utf-8 -*-
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.unittest import UnitTest


class CmdGetjid(SyncModule):
    def __init__(self, bot):
        desc = "getjid [nom]\nAffiche la première partie du jid pour découvrir qui se cache derrière un pseudo"
        SyncModule.__init__(self, 
                            bot, 
                            desc=desc,
                            command="getjid",
                            )

    @defaultcmd 
    def answer(self, sender, message):
        who = message or sender
        jid = self.bot.occupants.pseudo_to_jid(who)
        if jid == "":
            return "%s n'est pas dans le salon ou je n'ai pas le droit de lire les jid…" % who
        else:
            return jid


class GetjidTest(UnitTest):
    def __init__(self, bot):
        sender = "bob"
        cmd = (("!getjid", {"type": UnitTest.EXACT,
                            "expected": "%s n'est pas dans le salon ou je n'ai pas le droit de lire les jid…" % sender,
                            "sender": sender,
                            "desc": "!getjid [unknown user]"}),
               ("!getjid bob", {"type": UnitTest.EXACT,
                                "expected": "bob@domain.tld",
                                "sender": sender,
                                "pre_hook": self.create_user,
                                "post_hook": self.remove_user,
                                "desc": "!getjid bob avec bob enregistré"}),
                )
        UnitTest.__init__(self, cmd, bot, 'getjid')

    def create_user(self):
        self.bot.occupants.add_user("bob", "bob@domain.tld", "participant")

    def remove_user(self):
        self.bot.occupants.rm_user("bob")
