#-*- coding: utf-8 -*-
import os
from random import choice
from pipobot.lib.modules import ListenModule
from pipobot.lib import utils


class CmdKickGame(ListenModule):
    def __init__(self, bot):
        desc = "The bot will play with you, depending on your words..."
        ListenModule.__init__(self, bot, name="kick_game", desc=desc)
        path = os.path.join(os.path.dirname(__file__), 'list.txt')
        with open(path, 'r') as fichier:
            content = fichier.read()
            self.list_word = content.split("\n")
            self.word = choice(self.list_word)

    def answer(self, sender, message):
        if self.word in message.lower():
            if self.bot.occupants.pseudo_to_role(self.bot.name) in ['moderator', 'administrator']:
                if self.bot.occupants.pseudo_to_role(sender) in ['moderator', 'administrator']:
                    old_word = self.word
                    self.word = choice(self.list_word)
                    return "Il y a des gens qui mériterait un kick mais je ne peux pas le faire...\n%s: Tu as trouvé le mot caché qui était %s..." % (sender, old_word)
                else:
                    msg = u"Bravo, tu as trouvé le mot caché qui était %s, tu vas pouvoir te reposer hors du salon maintenant." % (self.word)
                    self.word = choice(self.list_word)
                    utils.kick(sender, msg, self.bot)
            else:
                old_word = self.word
                self.word = choice(self.list_word)
                return "%s: Je voudrais bien te kicker mais je n'en ai pas le droit :(. Tu as trouvé le mot caché qui était %s" % (sender, old_word)
