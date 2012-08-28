#! /usr/bin/env python
#-*- coding: utf-8 -*-
import random
from pipobot.lib.modules import SyncModule, defaultcmd

class CmdRoll(SyncModule):
    def __init__(self, bot):
        desc = """Le jugement des dieux !... Enfin de Pipo !
roll [entier] : renvoie un entier entre 1 et [entier]
roll [x,y,z] : renvoie un choix aléatoire entre x, y et z"""
        SyncModule.__init__(self,
                            bot, 
                            desc = desc,
                            command = "roll"
                            )
    
    @defaultcmd
    def answer(self, sender, message):
        if message.isdigit() and int(message) > 0:
            n = random.randint(1, int(message))
            return "%d !"%(n)
        elif message.strip() != "":
            return "%s !"%random.choice(message.split(","))
        else:
            return "Utilise un entier !"
