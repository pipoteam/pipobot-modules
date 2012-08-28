#! /usr/bin/env python
#-*- coding: utf-8 -*-

from pipobot.lib.modules import ListenModule
orig_ducks = [u"\_°<", u">°_/"]

class CmdCoin(ListenModule):
    def __init__(self, bot):
        desc = "Shooting ducks"
        ListenModule.__init__(self, bot,  name = "coin", desc = desc)
        self.ducks = list(orig_ducks)
        for eye in "0Oo":
            self.ducks.extend([duck.replace(u"°", eye) for duck in orig_ducks])
            

    def answer(self, sender, message) :
        if sender == self.bot.name :
            return
        if type(message) not in (str,unicode) :
            return
        coins = sum([message.count(duck) for duck in self.ducks])
        if coins > 0:
            pans = " ".join([u"*PAN*"]*coins)
            return u"%s : %s" % (sender, pans)
