#-*- coding: utf-8 -*-
import random
from . import repartie
import re
from pipobot.lib.modules import ListenModule
from pipobot.lib import utils


class CmdBot(ListenModule):
    def __init__(self, bot):
        desc = "The bot will not let you say anything about him !!"
        ListenModule.__init__(self, bot, name="repartie", desc=desc)
        self.question = repartie.question.split("\n")
        self.direct = repartie.direct.split("\n")
        self.indirect = repartie.indirect.split("\n")

    def answer(self, sender, message):
        if message[0] in ("", "!", ":"):
            return

        if re.search("^" + self.bot.name.lower() + r"(\W|$)", message.lower()):
            d = self.question if "?" in message else self.direct
            ret = random.choice(d)
            return "%s: %s" % (sender, ret)

        elif re.search(r"(^|\W)" + self.bot.name.lower() + r"($|\W)", message.lower()):
            ret = random.choice(self.indirect)
            return "%s: %s" % (sender, ret)

        elif re.search(r"\bsi\s+ils\b", message.lower()):
            return "%s: S'ILS, c'est mieux !!! :@" % sender

        elif re.search(r"\bsi\s+il\b", message.lower()):
            return "%s: S'IL, c'est mieux !!!" % sender

        elif re.search(r"(^|\s)+_all_(\!|\?|\:|\s+|$)", message.lower()):
            reply = self.bot.occupants.get_all(", ", [sender, self.bot.name])
            message = message.replace("_all_", reply)
            return message

        l = [["server", "serveur", "bot"], ["merde", "bois", "carton"]]
        if all([any([elt2 in message.lower() for elt2 in elt]) for elt in l]):
            msg = "Tu sais ce qu'il te dit le serveur ? Et puis surveille ton langage d'abord !!!"
            utils.kick(sender, msg, self.bot)
