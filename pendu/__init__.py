#! /usr/bin/env python
#-*- coding: utf-8 -*-
from pendu import Pendu
import os
import string
from pipobot.lib.modules import SyncModule, answercmd

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
        self.bot.pendu = Pendu("")

    @answercmd("init")
    def init(self, sender, args):
        if self.bot.pendu.word != "":
            return u"Il y a déjà une partie en cours… tu peux la finir, ou au pire 'reset' si tppt"
        if args == "":
            word_list = os.path.join(os.path.dirname(__file__), "wordlist.cfg")
            self.bot.pendu.word = self.bot.pendu.create_word(word_list)
            return u"Et c'est parti pour un pendu ! On cherche un mot de %s caractères" % len(self.bot.pendu.word)
        else:
            word = args.strip().lower()
            if all([letter in VALID_CAR for letter in word]):
                self.bot.pendu.word = word
                self.bot.say(u"Et c'est parti pour un pendu ! On cherche un mot de %s caractères" % len(self.bot.pendu.word))
            else:
                return u"Le mot choisi n'est pas valide ! (caractères acceptés : %s)" % VALID_CAR

    @answercmd("reset")
    def reset(self, sender, args):
        self.bot.pendu.word = ""
        return u"Reset effectué, plus qu'à utiliser init pour lancer une nouvelle partie"

    @answercmd("try", "guess")
    def guess(self, sender, args):
        if self.bot.pendu.word == "":
            return "Euh, il faudrait lancer une partie…"
        if len(args) == 1 and args in VALID_CAR:
            return self.bot.pendu.propose(args)
        else:
            return "Il faut proposer une lettre !"

    @answercmd("played", "histo")
    def played(self, sender, args):
        if self.bot.pendu.word == "":
            return "Euh, il faudrait lancer une partie…"
        return self.bot.pendu.playedtostr()
