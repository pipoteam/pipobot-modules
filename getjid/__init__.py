#-*- coding: utf-8 -*-
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.module_test import ModuleTest


class CmdGetjid(SyncModule):
    def __init__(self, bot):
        desc = (u"getjid [nom]\n"
                u"Affiche le jid pour découvrir qui se cache derrière un pseudo")
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


class GetjidUnknown(ModuleTest):
    def test_unknown_jid(self):
        sender = "bob"
        self.assertEqual(self.bot_answer("!getjid", user=sender),
                        "%s n'est pas dans le salon ou je n'ai pas le droit de lire les jid…" % sender)


class GetjidKnown(ModuleTest):
    sender = "bob"

    def test_known_jid(self):
        self.assertEqual(self.bot_answer("!getjid", user=self.sender),
                         "%s@domain.tld" % self.sender)
    
    def setUp(self):
        self.bot.occupants.add_user(self.sender,
                                    "%s@domain.tld" % self.sender,
                                    "participant")

    def tearDown(self):
        self.bot.occupants.rm_user(self.sender)
