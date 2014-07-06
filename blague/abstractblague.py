#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
from .model import Blagueur
from pipobot.lib.modules import SyncModule, defaultcmd


MIN_DELAY = 10


class AbstractBlague(SyncModule):
    """ Modifie les scores de blague """
    def __init__(self, bot, desc, name, autocongratulation, premier, operation):
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            pm_allowed=False,
                            name=name,
                           )
        self.autocongratulation = autocongratulation
        self.premier = premier  # S’utilise avec un %s pour le pseudo
        self.operation = operation

    @defaultcmd
    def answer(self, sender, message):
        if message == '':
            return self.desc

        jid = self.bot.occupants.pseudo_to_jid(message)
        if jid == "":
            return "%s n'est pas dans le salon !" % message

        reporter_jid = self.bot.occupants.pseudo_to_jid(sender)
        if reporter_jid == jid:
            return self.autocongratulation

        temps = int(time.time())
        res = self.bot.session.query(Blagueur).filter_by(pseudo=jid).first()

        if res is None:
            b = Blagueur(jid, self.operation(0, 1), temps)
            self.bot.session.add(b)
            send = self.premier % message
        else:
            MIN_DELAY = 10
            ecart = temps - res.submission
            if ecart > MIN_DELAY:
                date_bl = time.strftime("le %d/%m/%Y à %H:%M",
                                        time.localtime(float(res.submission)))
                res.score = self.operation(res.score, 1)
                res.submission = temps
                send = "Nouveau score - %s : %d\n%d secondes depuis ta dernière blague (%s)"
                send %= (message, res.score, ecart, date_bl)
            else:
                send = "Ta dernière blague date de moins de %s secondes !" % MIN_DELAY

        self.bot.session.commit()
        return send
