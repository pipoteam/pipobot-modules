# -*- coding: utf-8 -*-

import time

from pipobot.lib.modules import MultiSyncModule, defaultcmd


class CmdPingPong(MultiSyncModule):
    def __init__(self, bot):
        names = {"ping": "ping [pseudo]\nPing quelqu'un qui est sur le salon",
                 "pong": "pong [pseudo]\nRépond au ping de [pseudo]"}
        MultiSyncModule.__init__(self, bot, names=names)
        self.known_ping = {}

    @defaultcmd
    def answer(self, cmd, sender, message):
        list_pseudo = [user.nickname for user in self.bot.occupants.users.itervalues()]
        list_ping = message.split()
        list_intersect = set(list_ping).intersection(set(list_pseudo))
        if cmd == "ping":
            if list_intersect:
                for ping_name in list_intersect:
                    self.known_ping[sender + "_" + ping_name] = time.time()
                return "Ping %s" % (" ".join(list_intersect))
            return "%s: !help ping" % (sender)
        elif cmd == "pong":
            if list_intersect:
                ret = []
                for ping_name in list_intersect:
                    if (ping_name + "_" + sender) in self.known_ping:
                        time_ping = self.known_ping.pop(ping_name + "_" + sender)
                        t = time.time() - time_ping
                        ret.append("Tu as mis %s secondes pour répondre au ping de %s." % (str(int(t)), ping_name))
                if ret:
                    return "%s: %s" % (sender, "\n".join(ret))
            return "%s: !help pong" % (sender)
