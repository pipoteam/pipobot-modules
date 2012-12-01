#-*- coding: utf-8 -*-
import os
from random import choice
from pipobot.lib.modules import ListenModule
from pipobot.lib import utils


class CmdKickGame(ListenModule):
    def __init__(self, bot):
        desc = "The bot will play with you, depending on your words..."
        ListenModule.__init__(self, bot, name="kick_game", desc=desc)
        self.word = self.get_word()

    def answer(self, sender, message):
        if self.word in message.lower():
            old_word = self.word
            self.word = self.get_word()
            if self.bot.occupants.pseudo_to_role(self.bot.name) in ['moderator', 'administrator']:
                if self.bot.occupants.pseudo_to_role(sender) in ['moderator', 'administrator']:
                    return "Il y a des gens qui mériterait un kick mais je ne peux pas le faire...\n%s: Tu as trouvé le mot caché qui était %s..." % (sender, old_word)
                else:
                    msg = u"Bravo, tu as trouvé le mot caché qui était %s, tu vas pouvoir te reposer hors du salon maintenant." % (old_word)
                    utils.kick(sender, msg, self.bot)
            else:
                return "%s: Je voudrais bien te kicker mais je n'en ai pas le droit :(. Tu as trouvé le mot caché qui était %s" % (sender, old_word)

    def get_word(self):
        path = os.path.join(os.path.dirname(__file__), 'list.txt')
        with open(path, 'r') as word_file:
            content = word_file.read()
        return choice(content.split("\n"))

