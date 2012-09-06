#! /usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import time
import threading
import random
from pipobot.lib.modules import SyncModule, defaultcmd

class CmdTaggle(SyncModule):
    _config = (("default", str, ""),)

    def __init__(self, bot):
        desc = "Ta gueule [nom]\nDit taggle à nom (valeur par défaut à mettre dans le fichier de configuration)"
        SyncModule.__init__(self, 
                            bot, 
                            desc = desc,
                            command = "tg",
                            )

    @defaultcmd 
    def answer(self, sender, message):
        if sender.lower() == self.default.lower() and message == '':
            toalmostall = self.bot.occupants.get_all(" ", [self.bot.name, sender])
            return u"%s: Fermez tous voggle !!!"%(toalmostall)
        else:
            if message == '':
                if self.default == "":
                    return u"EUH, taggle qui ?"
                else:
                    return u"Taggle %s" % self.default
            elif self.bot.name.lower() in message.lower():
                r = random.random()
                if r < 0.1:
                    self.bot.say(u"Ouais ouais et puis quoi encore ?!")
                else:
                    self.bot.say(u"Bon bah puisque c'est comme ça je boude")
                    self.bot.mute = True
                    self.bot.t = threading.Timer(30.0, self.bot.disable_mute)
                    self.bot.t.start()
                return ""
            elif message.lower() == sender.lower():
                return u"Non mais vraiment ... taggle ! Au lieu de me faire dire n'importe quoi !"
            else:
                return u"Taggle %s" % message
