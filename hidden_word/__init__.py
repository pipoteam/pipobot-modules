#-*- coding: utf-8 -*-
import os
import time
from random import choice
from sqlalchemy.sql.expression import desc
from model import HiddenBase
from pipobot.lib.modules import ListenModule, defaultcmd
from pipobot.lib import utils


class CmdHiddenWord(ListenModule):
    def __init__(self, bot):
        desc = "Un petit jeu où il faut trouver le mot que le bot aura choisi"
        ListenModule.__init__(self, bot, name="hidden_word", desc=desc)
        self.word = self.get_word()

    @defaultcmd
    def answer(self, sender, message):
        if self.word in message.lower():
            msg = u"Bravo %s, tu as trouvé le mot caché qui était %s. Tu peux te reposer maintenant." % (sender, self.word)
            self.word = self.get_word()

            jid = self.bot.occupants.pseudo_to_jid(sender.strip())
            res = self.bot.session.query(HiddenBase).filter(HiddenBase.jid == jid).all()
            if len(res) == 0:
                r = HiddenBase(jid, 1)
                self.bot.session.add(r)
            else:
                hid = res[0]
                hid.score += 1
            self.bot.session.commit()
            return msg

    def get_word(self):
        path = os.path.join(os.path.dirname(__file__), 'list.txt')
        with open(path, 'r') as word_file:
            content = word_file.read()
        return choice(content.split("\n"))

    def cmd_score(self, sender, message):
        classement = self.bot.session.query(HiddenBase).order_by(desc(HiddenBase.score)).all()

        if classement != []:
            sc = "\nHidden Word Score :"
            pseudo = ""
            sc += "\n┌" + 39 * "─" + "┐"
            for hidden in classement:
                pseudo = self.bot.occupants.jid_to_pseudo(hidden.jid)
                sc += "\n│ %-4s - %-30s │" % (hidden.score, pseudo)
            sc += "\n└" + 39 * "─" + "┘"
            return {"text": sc, "monospace": True}
        else:
            return "Aucun mot caché trouvé..."
