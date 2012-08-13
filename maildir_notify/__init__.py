# -*- coding: utf8 -*-

from email.header import decode_header
from email.parser import Parser
from os.path import isdir, isfile, join
import os
import pwd
import pyinotify
import time

from pipobot.lib.modules import AsyncModule


class MailNotify(AsyncModule, pyinotify.ProcessEvent):
    def __init__(self, bot):

        AsyncModule.__init__(self, bot, name="mail_notify",
            desc="Displaying incoming mails", delay=0)
        pyinotify.ProcessEvent.__init__(self)

        self._parser = Parser()

        pw_dir = pwd.getpwuid(os.getuid()).pw_dir
        path = join(pw_dir, "Maildir", "new")

        if not isdir(path):
            raise RuntimeError("%s is missing" % path)

        self.destpath = join(pw_dir, "Maildir", "cur")
        for item in os.listdir(path):
            item_path = join(path, item)
            if isfile(item_path):
                os.rename(item_path, join(self.destpath, item))

        wmng = pyinotify.WatchManager()
        self.notifier = pyinotify.Notifier(wmng, self)
        wmng.add_watch(path, pyinotify.IN_MOVED_TO | pyinotify.IN_CREATE)

    def cleanup(self):
        limit = time.time() - 7 * 86400
        for item in os.listdir(self.destpath):
            item_path = join(self.destpath, item)

            if isfile(item_path) and os.stat(item_path).st_mtime < limit:
                os.remove(item_path)

    @staticmethod
    def decode(header):
        if not header:
            return ""

        result = ""
        for data, charset in decode_header(header):
            if charset is None:
                charset = "ascii"

            try:
                result += data.decode(charset, 'replace')
            except LookupError:
                result += data.decode('utf-8', 'replace')

        return result

    def process_default(self, event):
        try:
            with open(event.pathname, 'r') as handle:
                data = handle.read()
        except IOError:
            return

        message = self._parser.parsestr(data, headersonly=True)
        msg_subject = self.decode(message['Subject'])
        msg_from = self.decode(message['From'])
        msg_spam = message['X-Spam-Score'] or ""
        try:
            msg_spam = float(msg_spam)
        except ValueError:
            msg_spam = None

        if not msg_subject:
            msg_subject = "[???]"

        if not msg_from:
            msg_from = "<???>"

        result = u">> Mail de %s : %s" % (msg_from, msg_subject)
        if msg_spam is not None:
            result += u" (Spam Score: %.1f)" % msg_spam

        if msg_spam is None or msg_spam < 0.0:
            self.bot.say(result)

        os.rename(event.pathname, join(self.destpath, event.name))
        self.cleanup()

    def action(self):
        self.notifier.process_events()
        if self.notifier.check_events():
            self.notifier.read_events()

