# -*- coding: utf-8 -*-
import random
import re

from pipobot.lib import utils
from pipobot.lib.modules import ListenModule

import repartie


class CmdBot(ListenModule):
    def __init__(self, bot):
        desc = "The bot will not let you say anything about him !!"
        ListenModule.__init__(self, bot, name="repartie", desc=desc)

    def answer(self, sender, message):
        if type(message) not in (str, unicode):
            return
        if message == "":
            return
        if message[0] in ["!", ":"]:
            return
        if re.search("^" + self.bot.name.lower() + "(\W|$)", message.lower()):
            if '?' in message:
                d = repartie.question.split("\n")
            else:
                d = repartie.direct.split("\n")
            random.shuffle(d)
            return u"%s: %s" % (sender, d[0])
        elif re.search("(^|\W)" + self.bot.name.lower() + "($|\W)", message.lower()):
            i = repartie.indirect.split("\n")
            random.shuffle(i)
            return u"%s: %s" % (sender, i[0])
        elif re.search("\bsi\s+ils\b", message.lower()):
            return u"%s: S'ILS, c'est mieux !!! :@" % sender
        elif re.search("\bsi\s+il\b", message.lower()):
            return u"%s: S'IL, c'est mieux !!!" % sender
        elif re.search("(^|\s)+_all_(\!|\?|\:|\s+|$)", message.lower()):
            reply = self.bot.occupants.get_all(", ", [sender, self.bot.name])
            message = message.replace("_all_", reply)
            return message
        l = [["server", "serveur", "bot"], ["merde", "bois", "carton"]]
        if all([any([elt2 in message.lower() for elt2 in elt]) for elt in l]):
            msg = u"Tu sais ce qu'il te dit le serveur ? Et puis surveille ton langage d'abord !!!"
            utils.kick(sender, msg, self.bot)
