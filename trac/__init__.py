#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlite3
from pipobot.lib.modules import SyncModule, defaultcmd


class CmdTrac(SyncModule):
    _config = (("db_path", str, None),)

    def __init__(self, bot):
        desc = "trac [num]\nListe les tickets trac actifs ou en affiche un en détail"
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="trac",
                            )

    @defaultcmd
    def answer(self, sender, message):
        send = "\n"
        # Connection db
        if self.db_path == "":
            return u"Ma configuration ne me permet pas de répondre à cette question…"

        conn = sqlite3.connect(self.db_path)
        conn.isolation_level = None
        c = conn.cursor()
        if message == '':
            c.execute("SELECT id, priority, summary FROM ticket WHERE status!='closed' ORDER BY priority")
            for id, p, summary in c.fetchall():
                send += "[%d] %s\n" % (id, summary)
            if send == "\n":
                send = u"Pas de ticket ! Vous avez plus qu'à espérer ne pas vous faire contrôler"

        else:
            try:
                i = int(message)
            except:
                return u"Merci de rentrer un numéro de ticket"
            c.execute("SELECT id, priority, summary, description FROM ticket WHERE id=? ORDER BY priority", (i,))
            id, p, summ, desc = c.fetchone()
            send += "[%d] %s\n%s\n" % (id, summ, desc)
        conn.commit()
        conn.close()
        return send.rstrip()
