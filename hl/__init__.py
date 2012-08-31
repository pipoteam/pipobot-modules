#! /usr/bin/env python
#-*- coding: utf-8 -*-

from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.known_users import KnownUser


class HighLight(SyncModule):
    def __init__(self, bot):
        desc = _("Highligh people")
        SyncModule.__init__(self,
                bot,
                desc=desc,
                command='hl')

    @defaultcmd
    def answer(self, sender, message):
        knownusers = []
        unknownusers = []
        ret = self.desc
        for user in message.split(' '):
            knownuser = KnownUser.get(user, self.bot)
            if knownuser:
                knownusers.append(knownuser)
            else:
                unknownusers.append(user)
        if knownusers or unknownusers:
            ret = 'HL: '
            for user in self.bot.occupants.users:
                if KnownUser.get(user, self.bot) in knownusers:
                    ret += '%s ' % user
            if unknownusers:
                ret += '− Unknown: '
                for user in unknownusers:
                    ret += '%s ' % user
        return ret
