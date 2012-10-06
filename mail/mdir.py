# -*- coding: utf8 -*-

"""
Mail notifier for Linux systems using Maildir mailboxes
"""

import os
import pwd
import pyinotify
import time
from email.parser import Parser
from os.path import isdir, isfile, join

from tools import decode


class MdirNotify(pyinotify.ProcessEvent):
    """
    Main module class.
    """

    def __init__(self, bot, path=""):

        pyinotify.ProcessEvent.__init__(self)

        self.bot = bot
        self._parser = Parser()

        pw_dir = path
        if path == "":
            pw_dir = pwd.getpwuid(os.getuid()).pw_dir


        path = join(pw_dir, "Maildir", bot.chatname.split('@')[0], "new")
        self.destpath = join(pw_dir, "Maildir", bot.chatname.split('@')[0], "cur")
        if not isdir(path) or not isdir(self.destpath):
            path = join(pw_dir, "Maildir", "new")
            self.destpath = join(pw_dir, "Maildir", "cur")
        if not isdir(path):
            raise RuntimeError("%s is missing" % path)

        for item in os.listdir(path):
            item_path = join(path, item)
            if isfile(item_path):
                os.rename(item_path, join(self.destpath, item))

        wmng = pyinotify.WatchManager()
        self.notifier = pyinotify.Notifier(wmng, self)
        wmng.add_watch(path, pyinotify.IN_MOVED_TO | pyinotify.IN_CREATE)

    def cleanup(self):
        """
        Remove week-old mails from the mailbox
        """
        limit = time.time() - 7 * 86400
        for item in os.listdir(self.destpath):
            item_path = join(self.destpath, item)

            if isfile(item_path) and os.stat(item_path).st_mtime < limit:
                os.remove(item_path)

    def process_default(self, event):
        """
        Called when a new mail is received and placed in Maildir’s new mail
        folder.
        """

        try:
            with open(event.pathname, 'r') as handle:
                data = handle.read()
        except IOError:
            return

        message = self._parser.parsestr(data, headersonly=True)
        msg_subject = decode(message['Subject'])
        msg_from = decode(message['From'])
        msg_spam = message['X-Spam-Score'] or ""
        try:
            msg_spam = float(msg_spam)
        except ValueError:
            msg_spam = None

        if not msg_subject:
            msg_subject = u"[Pas de sujet]"

        if not msg_from:
            msg_from = u"<Pas d’expéditeur>"

        result = u">> Mail de %s : %s" % (msg_from, msg_subject)
        if msg_spam is not None:
            result += u" (Spam Score: %.1f)" % msg_spam

        if msg_spam is None or msg_spam < 0.0:
            self.bot.say(result)

        os.rename(event.pathname, join(self.destpath, event.name))
        self.cleanup()

    def action(self):
        """
        The inotify event loop.
        """

        self.notifier.process_events()
        if self.notifier.check_events():
            self.notifier.read_events()
