#-*- coding: utf-8 -*-
import core
from pipobot.lib.modules import MultiSyncModule, defaultcmd
from pipobot.lib.module_test import ModuleTest


class CmdNextPrev(MultiSyncModule):
    def __init__(self, bot):
        names = {"next": "next [show1;show2;show3]\nAffiche les infos sur le prochain épisode en date de show1,show2,show3",
                    "prev": "prev [show1;show2;show3]\nAffiche les infos sur le dernier épisode en date de show1,show2,show3"}
        MultiSyncModule.__init__(self,
                                 bot,
                                 names=names)

    @defaultcmd
    def answer(self, cmd, sender, message):
        return core.getdata(message, cmd=="next")


class NextPrevTest(ModuleTest):
    def test__next(self):
        bot_rep = self.bot_answer("!next tbbt")
        self.assertRegexpListMatches(bot_rep,
                                     ["Prochain épisode de The Big Bang Theory: (.*)",
                                      "Aucune date pour un prochain épisode :s."])

        bot_rep = self.bot_answer("!prev himym")
        self.assertRegexpListMatches(bot_rep,
                                     ["Précédent épisode de How I Met Your Mother: (.*)",
                                      "Aucune info disponible."])

    def test_ended(self):
        bot_rep = self.bot_answer("!next chuck")
        self.assertEqual(bot_rep, u"Désolé mais la série Chuck est terminée.")

    def test_failed(self):
        bot_rep = self.bot_answer("!next qsdf")
        self.assertEqual(bot_rep, u"Je n'ai aucune information sur la série qsdf")
