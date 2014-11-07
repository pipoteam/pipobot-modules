#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
from model import GoreBase
from pipobot.lib.modules import SyncModule, defaultcmd
from sqlalchemy import func
from sqlalchemy.sql.expression import desc


class CmdGore(SyncModule):
    """ Ajoute un point-gore à une personne présente sur le salon"""
    def __init__(self, bot):
        desc = u"gore <pseudo>\nAjoute un point gore à <pseudo> (10 s minimum d'intervalle)"
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            pm_allowed=False,
                            name="gore",
                            )

    @defaultcmd
    def answer(self, sender, message):
        send = ''
        if message == '':
            return u"Vous devez donner un point gore à une personne -> !gore <pseudo>"
        sjid = self.bot.occupants.pseudo_to_jid(sender.strip())
        jid = self.bot.occupants.pseudo_to_jid(message)
        if jid == "":
            return u"%s n'est pas là..." % message

        if sjid == jid:
            return u"On ne peut pas se donner des points gore !"

        temps = int(time.time())
        res = self.bot.session.query(GoreBase).filter(GoreBase.jid == jid).all()

        if len(res) == 0:
            send = u"Félicitations %s, c'est ton premier point gore !" % (message)
            r = GoreBase(jid, 1, temps)
            self.bot.session.add(r)
        else:
            gore = res[0]
            ecart = temps - int(gore.submission)
            if ecart > 10:
                gore.score += 1
                date_bl = time.strftime("le %d/%m/%Y a %H:%M",
                                        time.localtime(float(gore.submission)))
                send = u"Nouveau score - %s : %d\n%d secondes depuis ton dernier point gore (%s)" % (message, gore.score, ecart, date_bl)
                gore.submission = temps
        self.bot.session.commit()
        return send

    def cmd_score(self, sender, message):
        """Affiche les scores des points gore"""
        classement = self.bot.session.query(GoreBase).order_by(desc(GoreBase.score)).all()

        if classement != []:
            sc = "\nGore - scores :"
            pseudo = ""
            sc += "\n┌" + 72 * "─" + "┐"
            for gore in classement:
                sc += "\n│ %-4s  -  " % (gore.score)
                pseudo = self.bot.occupants.jid_to_pseudo(gore.jid)

                if len(pseudo) > 30:
                    sc += "%s " % (pseudo[:30])
                else:
                    sc += "%-30s " % (pseudo)

                sc += time.strftime(" dernier le %d/%m/%Y à %H:%M │", time.localtime(gore.submission))
            sc += "\n└" + 72 * "─" + "┘"
            return {"text": sc, "monospace": True}
        else:
            return "Aucun point gore..."

