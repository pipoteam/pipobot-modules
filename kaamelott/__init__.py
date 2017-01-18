# -*- coding: utf-8 -*-
import os
import random

from pipobot.lib.modules import MultiSyncModule, defaultcmd
from pipobot.lib.utils import ListConfigParser


class Kaamelott(MultiSyncModule):
    def __init__(self, bot):
        names = self.readconf()
        MultiSyncModule.__init__(self,
                                 bot,
                                 names=names)

    def readconf(self):
        config_file = os.path.join(os.path.dirname(__file__), 'kaamelott.cfg')
        names = {}
        self.dico = {}
        config = ListConfigParser()
        config.read(config_file)
        self.genericCmd = config.sections()
        for c in self.genericCmd:
            command_name = c.decode("utf-8")
            self.dico[command_name] = {}
            self.dico[command_name]['desc'] = config.get(c, 'desc')
            quote = config.get(c, 'citation')
            self.dico[command_name]['citation'] = quote if type(quote) is list else [config.get(c, 'citation')]
            names[command_name] = self.dico[command_name]['desc']
        return names

    @defaultcmd
    def answer(self, cmd, sender, message):
        if cmd == '':
            return u"Il faut mettre une personne parmi la liste que tu peux aller voir tout seul dans le help !"
        elif message == '':
            return random.choice(self.dico[cmd]["citation"]).decode("utf-8")
        else:
            return u"Pourquoi un argument ?"
