#! /usr/bin/env python
#-*- coding: utf-8 -*-
import random
from pendu import Pendu
from pipobot.lib.modules import SyncModule, answercmd

class CmdPendu(SyncModule):
    def __init__(self, bot):
        desc = """Un superbe jeu de pendu
pendu init : lance une partie avec un mot aléatoire (to be coded...)
pendu init [word] : lance une partie avec 'word' comme mot à trouver
pendu try [letter] : propose la lettre 'letter'
pendu played : affiche la liste des lettres déjà jouées"""
        SyncModule.__init__(self, 
                                bot, 
                                desc = desc,
                                command = "pendu")
        self.bot.pendu = Pendu("")

    #TODO rewrite using decorators
    @answercmd("init")
    def init(self, sender, args):
        if args == "":
            self.bot.pendu.word = self.bot.pendu.create_word(self.bot.module_path["pendu"])
        else:
            self.bot.pendu.word = args.strip().lower()
        self.bot.say("Et c'est parti pour un pendu !")

    @answercmd("try", "guess")
    def guess(self, sender, args):
        if args == "" or len(args) > 1:
            return "Il faut proposer une lettre !"
        else:
            return self.bot.pendu.propose(args.lower())

    @answercmd("played", "histo")
    def played(self, sender, args):
        return self.bot.pendu.playedtostr()
