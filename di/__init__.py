# -*- encoding: utf-8 -*-
from pipobot.lib.modules import ListenModule


class DiAnswer(ListenModule):
    def __init__(self, bot):
        desc = "Pipo dit"
        ListenModule.__init__(self, bot, name="dianswer", desc=desc)

    def answer(self, sender, message):
        message = message.lower()
        for di in ["di", "dy", "d'y", u"d’y"]:
            if di in message:
                return message.split(di, 1)[1]
