# -*- coding: utf-8 -*-

import time

from tools import decode

DEFAULT_FILE = '/var/mail/bot'


class MboxNotify:
    """ A notifier for mbox format """
    def __init__(self, bot, path=""):
        self.bot = bot
        if path == "":
            path = DEFAULT_FILE

        box_file = open(path, "w")
        box_file.write('')
        box_file.close()

        self.file = open(path)
        self.msubject = ""
        self.mfrom = ""
        self.spam = -1

    def action(self):
        t = self.file.readline()
        if t == '':
            time.sleep(1)
        elif t[:5] == "From:":
            self.mfrom = decode(t[5:].strip())
        elif t[:8] == "Subject:":
            self.msubject = decode(t[8:].strip())
        elif t[:13] == "X-Spam-Score:":
            try:
                self.spam = float(t[14:].strip())
            except:
                self.spam = -2
        elif t[:14] == "X-Spam-Status:":
            try:
                self.spam = float(t[14:].split("=")[1].split()[0].strip())
            except:
                self.spam = -2

        if self.mfrom != "" and self.msubject != "":
            if self.spam < 0:
                try:
                    self.bot.say(">> Mail de %s : %s (Spam Score : %f)" %
                                 (self.mfrom, self.msubject, self.spam))
                except:
                    self.bot.say(">> Mail de %s : <encodage foireux> (Spam Score : %f)" %
                                 (self.mfrom, self.spam))
            self.mfrom = ""
            self.msubject = ""
            self.spam = -1
