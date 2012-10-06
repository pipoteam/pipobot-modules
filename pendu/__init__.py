#! /usr/bin/env python
#-*- coding: utf-8 -*-
import os
import string
from pipobot.lib.modules import SyncModule, answercmd
from pipobot.lib.module_test import ModuleTest
from pendu import Pendu
from pendu_ascii import asc_res


VALID_CAR = string.ascii_lowercase + "-'"


class CmdPendu(SyncModule):
    def __init__(self, bot):
        desc = u"""Un superbe jeu de pendu
pendu init : lance une partie avec un mot aléatoire (to be coded...)
pendu init [word] : lance une partie avec 'word' comme mot à trouver
pendu reset : pour interrompre une partie en cours
pendu try [letter] : propose la lettre 'letter'
pendu played : affiche la liste des lettres déjà jouées"""
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            command="pendu")
        self.pendu = Pendu("")

    @answercmd("init", "init (?P<word>\w+)")
    def init(self, sender, word=""):
        if self.pendu.word != "":
            return u"Il y a déjà une partie en cours… tu peux la finir, ou au pire 'reset' si tppt"

        if word == "":
            word_list = os.path.join(os.path.dirname(__file__), "wordlist.cfg")
            self.pendu.word = self.pendu.create_word(word_list)
            return u"Et c'est parti pour un pendu ! On cherche un mot de %s caractères" % len(self.pendu.word)
        else:
            word = word.strip().lower()
            if all([letter in VALID_CAR for letter in word]):
                self.pendu.word = word
                self.bot.say(u"Et c'est parti pour un pendu ! On cherche un mot de %s caractères" % len(self.pendu.word))
            else:
                return u"Le mot choisi n'est pas valide ! (caractères acceptés : %s)" % VALID_CAR

    @answercmd("reset")
    def reset(self, sender):
        self.pendu.word = ""
        return u"Reset effectué, plus qu'à utiliser init pour lancer une nouvelle partie"

    @answercmd("(try|guess) (?P<letter>\w)")
    def guess(self, sender, letter):
        if self.pendu.word == "":
            return "Euh, il faudrait lancer une partie…"

        if letter in VALID_CAR:
            return self.pendu.propose(letter)
        else:
            return "Il faut proposer une lettre !"

    @answercmd("(played|histo)")
    def played(self, sender):
        if self.pendu.word == "":
            return u"Euh, il faudrait lancer une partie…"
        return self.pendu.playedtostr()


class PenduTest(ModuleTest):
    def test_pendu_success(self):
        """Pendu scenario where the user finds the answer !"""
        self.assertEqual(self.bot_answer("!pendu reset"),
                         u"Reset effectué, plus qu'à utiliser init pour lancer une nouvelle partie")
        self.assertEqual(self.bot_answer("!pendu played"),
                         u"Euh, il faudrait lancer une partie…")

        bot_rep = self.bot_answer("!pendu init pipoteam")
        ok_tests = [("p", "p_p_____"), ("i", "pip_____"), ("e", "pip__e__")]
        for letter, state in ok_tests:
            bot_rep = self.bot_answer("!pendu try %s" % letter)
            self.assertEqual(bot_rep, u"Bien vu ! Mot actuel: %s" % state)

        self.assertEqual(self.bot_answer("!pendu try p"),
                         u"Lettre déjà proposée")

        expected = u"%s\nMot actuel : %s" % (asc_res[0], "pip__e__")
        self.assertEqual(self.bot_answer("!pendu try z"),
                         expected)

        self.assertEqual(self.bot_answer("!pendu histo"),
                         u"Lettres jouées: e, i, p, z")

        ok_tests = [("o", "pipo_e__"), ("t", "pipote__"), ("a", "pipotea_")]
        for letter, state in ok_tests:
            bot_rep = self.bot_answer("!pendu try %s" % letter)
            self.assertEqual(bot_rep, u"Bien vu ! Mot actuel: %s" % state)

        bot_rep = self.bot_answer("!pendu try m")
        self.assertEqual(bot_rep, u"Bien vu !\nEt oui, le mot à trouver était bien pipoteam !")

    def try_8_wrong(self):
        self.assertEqual(self.bot_answer("!pendu reset"),
                         u"Reset effectué, plus qu'à utiliser init pour lancer une nouvelle partie")
        bot_rep = self.bot_answer("!pendu init pipoteam")
        for (index, letter) in enumerate("zryuqsdf"):
            expected = u"%s\nMot actuel : %s" % (asc_res[index], "________")
            self.assertEqual(self.bot_answer("!pendu try %s" % letter),
                             expected)

    def test_pendu_fail(self):
        """Pendu scenario where the user does not find the answer !"""
        self.try_8_wrong()
        expected = "%sTu devais trouver pipoteam" % asc_res[8]
        self.assertEqual(self.bot_answer("!pendu try k"),
                         expected)

    def test_last_minute_success(self):
        """Finds the answer of the pendu at the last try !!"""
        self.try_8_wrong()
        ok_tests = [("p", "p_p_____"), ("i", "pip_____"), ("e", "pip__e__")]
        ok_tests += [("o", "pipo_e__"), ("t", "pipote__"), ("a", "pipotea_")]
        for letter, state in ok_tests:
            bot_rep = self.bot_answer("!pendu try %s" % letter)
            self.assertEqual(bot_rep, u"Bien vu ! Mot actuel: %s" % state)
        bot_rep = self.bot_answer("!pendu try m")
        self.assertEqual(bot_rep, u"Bien vu !\nEt oui, le mot à trouver était bien pipoteam !")
