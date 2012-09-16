#! /usr/bin/env python
#-*- coding: utf-8 -*-
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.unittest import GroupUnitTest, ExactTest


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


class GetjidTest(GroupUnitTest):
    def __init__(self, bot):
        sender = "bob"
        tst = ExactTest(cmd="!getjid",
                        expected="%s n'est pas dans le salon ou je n'ai pas le droit de lire les jid…" % sender,
                        desc="!getjid [unknown user]",
                        sender=sender)
        tst2 = ExactTest(cmd="!getjid bob",
                         expected="bob@domain.tld",
                         desc=u"!getjid avec utilisateur enregistré",
                         sender=sender,
                         pre_hook=lambda: self.create_user(sender),
                         post_hook=lambda: self.remove_user(sender))

        GroupUnitTest.__init__(self, [tst, tst2], bot, 'getjid')

    def create_user(self, sender):
        self.bot.occupants.add_user(sender, "%s@domain.tld" % sender, "participant")

    def remove_user(self, sender):
        self.bot.occupants.rm_user(sender)
