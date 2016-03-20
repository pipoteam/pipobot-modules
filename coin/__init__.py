# -*- coding: utf-8 -*-

from pipobot.lib.module_test import ModuleTest
from pipobot.lib.modules import ListenModule

orig_ducks = [u"\_°<", u">°_/"]


class CmdCoin(ListenModule):
    def __init__(self, bot):
        desc = "Shooting ducks"
        ListenModule.__init__(self, bot, name="coin", desc=desc)
        self.ducks = list(orig_ducks)
        for eye in u"0Oo+":
            self.ducks.extend([duck.replace(u"°", eye) for duck in orig_ducks])

    def answer(self, sender, message):
        coins = sum([message.count(duck) for duck in self.ducks])
        if coins > 0:
            pans = (" *PAN*" * coins).strip()
            return u"%s : %s" % (sender, pans)


class TestCoin(ModuleTest):
    def test_ok(self):
        rep = self.bot_answer("\_°< \_O< >o_/ \_+<", "bob")
        self.assertEqual(rep,
                         u"bob : *PAN* *PAN* *PAN* *PAN*")

    def test_none(self):
        rep = self.bot_answer("a duck-free message")
        self.assertEqual(rep, "")
