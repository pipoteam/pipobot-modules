#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pipobot.lib.modules import ListenModule
from datetime import datetime
import random
import re


class Troll(ListenModule):
    _config = (('words', list, []),)

    def __init__(self, bot):
        desc = u"Pipo n'aime pas les trolls."
        ListenModule.__init__(self, bot, name='troll', desc=desc)
        self.words = [w.lower() for w in self.words]

    def answer(self, sender, message):
        if any(w.lower() in self.words for w in re.findall(r'[a-zA-Z]+', message)):
            if datetime.now().weekday() == 4: # Friday
                return random.choice([
                    u"Oh un troll … wait … mais on est vendredi ! Personnellement, je pense que ton truc, c'est de la grosse merde.",
                    u'Happy Troll Day !',
                    u"Pas de troll en semaine, merci. Mais non, je déconne, c'est vendredi, c'est le week-end !!",
                    None, # no answer
                ])
            else:
                return random.choice([
                    u'Hum.. ça sent le troll !',
                    u'Stop le troll !',
                    u'TROLLLLLLLLLLLLLLLLLLL !',
                    u'Troll spotted !',
                    u'Pas de troll en semaine, merci. Il y a des gens qui bossent ! (ou pas)',
                ])
