#! /usr/bin/env python
#-*- coding: utf-8 -*-
from pendu import Pendu
import os
import string
from pipobot.lib.modules import SyncModule, answercmd

class CmdPendu(SyncModule):
    def __init__(self, bot):
        desc = u"""Un superbe jeu de pendu
pendu init : lance une partie avec un mot aléatoire (to be coded...)
pendu init [word] : lance une partie avec 'word' comme mot à trouver
pendu try [letter] : propose la lettre 'letter'
pendu played : affiche la liste des lettres déjà jouées"""
        SyncModule.__init__(self, 
                                bot, 
                                desc = desc,
                                command = "pendu")
        self.bot.pendu = Pendu("")

    @answercmd("init")
    def init(self, sender, args):
        if args == "":
            word_list = os.path.join(os.path.dirname(__file__), "wordlist.cfg")
            self.bot.pendu.word = self.bot.pendu.create_word(word_list)
        else:
            self.bot.pendu.word = args.strip().lower()
        return u"Et c'est parti pour un pendu ! On cherche un mot de %s caractères" % len(self.bot.pendu.word)

    @answercmd("try", "guess")
    def guess(self, sender, args):
        if self.bot.pendu.word == "":
            return "Euh, il faudrait lancer une partie…"
        if len(args) == 1 and args in string.ascii_lowercase:
            return self.bot.pendu.propose(args)
        else:
            return "Il faut proposer une lettre !"

    @answercmd("played", "histo")
    def played(self, sender, args):
        if self.bot.pendu.word == "":
            return "Euh, il faudrait lancer une partie…"
        return self.bot.pendu.playedtostr()
