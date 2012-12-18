#-*- coding: utf-8 -*-
import random
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.module_test import ModuleTest


class CmdRoll(SyncModule):
    def __init__(self, bot):
        desc = """Le jugement des dieux !... Enfin de Pipo !
roll [entier] : renvoie un entier entre 1 et [entier]
roll [x,y,z] : renvoie un choix aléatoire entre x, y et z"""
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="roll"
                            )

    @defaultcmd
    def answer(self, sender, message):
        if message.isdigit() and int(message) > 0:
            n = random.randint(1, int(message))
            return "%d !" % n
        elif message.strip() != "":
            return "%s !" % random.choice(message.split(",")).strip()
        else:
            return "Utilise un entier ou une liste séparée par des «,»"


class TestRoll(ModuleTest):
    def test_int(self):
        rep = self.bot_answer("!roll 42")
        self.assertRegexpMatches(rep,
                                 r"\d{1,2} !")

    def test_list(self):
        rep = self.bot_answer("!roll pipo, pouet, blabla")
        self.assertIn(rep, ["pipo !", "pouet !", "blabla !"])
