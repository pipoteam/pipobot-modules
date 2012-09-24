# -*- coding: utf8 -*-

"""
Mail notifier for Linux systems using Maildir mailboxes
"""

from email.errors import HeaderParseError
from email.parser import Parser
from os.path import isdir, isfile, join
import binascii
import email.base64mime
import email.quoprimime
import os
import pwd
import pyinotify
import re
import time

from pipobot.lib.modules import AsyncModule

# The following code is from the email.header file, modified to correctly
# handle the decoding of some specific headers. (See Python bug #1079,
# http://bugs.python.org/issue1079)

ECRE = re.compile(r'''
  =\?                   # literal =?
  (?P<charset>[^?]*?)   # non-greedy up to the next ? is the charset
  \?                    # literal ?
  (?P<encoding>[qb])    # either a "q" or a "b", case insensitive
  \?                    # literal ?
  (?P<encoded>.*?)      # non-greedy up to the next ?= is the encoded string
  \?=                   # literal ?=
  ''', re.VERBOSE | re.IGNORECASE | re.MULTILINE)


def decode_header(header):
    """Decode a message header value without converting charset.

    Returns a list of (decoded_string, charset) pairs containing each of the
    decoded parts of the header.  Charset is None for non-encoded parts of the
    header, otherwise a lower-case string containing the name of the character
    set specified in the encoded string.

    An email.errors.HeaderParseError may be raised when certain decoding error
    occurs (e.g. a base64 decoding exception).
    """
    # If no encoding, just return the header
    header = str(header)
    if not ECRE.search(header):
        return [(header, None)]
    decoded = []
    dec = ''
    for line in header.splitlines():
        # This line might not have an encoding in it
        if not ECRE.search(line):
            decoded.append((line, None))
            continue
        parts = ECRE.split(line)
        first = True
        while parts:
            unenc = parts.pop(0)
            if first:
                unenc = unenc.lstrip()
                first = False
            if unenc:
                # Should we continue a long line?
                if decoded and decoded[-1][1] is None:
                    decoded[-1] = (decoded[-1][0] + " " + unenc, None)
                else:
                    decoded.append((unenc, None))
            if parts:
                charset, encoding = [s.lower() for s in parts[0:2]]
                encoded = parts[2]
                dec = None
                if encoding == 'q':
                    dec = email.quoprimime.header_decode(encoded)
                elif encoding == 'b':
                    paderr = len(encoded) % 4  # add missing padding
                    if paderr:
                        encoded += '==='[:4 - paderr]
                    try:
                        dec = email.base64mime.decode(encoded)
                    except binascii.Error:
                        # Turn this into a higher level exception.  BAW: Right
                        # now we throw the lower level exception away but
                        # when/if we get exception chaining, we'll preserve it.
                        raise HeaderParseError
                if dec is None:
                    dec = encoded

                if decoded and decoded[-1][1] == charset:
                    decoded[-1] = (decoded[-1][0] + dec, decoded[-1][1])
                else:
                    decoded.append((dec, charset))
            del parts[0:3]
    return decoded

# End of modified code from email.header code


class MailNotify(AsyncModule, pyinotify.ProcessEvent):
    """
    Main module class.
    """

    def __init__(self, bot):

        AsyncModule.__init__(self, bot, name="mail_notify",
                             desc="Displaying incoming mails", delay=0)
        pyinotify.ProcessEvent.__init__(self)

        self._parser = Parser()

        pw_dir = pwd.getpwuid(os.getuid()).pw_dir

        path = join(pw_dir, "Maildir", bot.chatname, "new")
        self.destpath = join(pw_dir, "Maildir", bot.chatname, "cur")
        if not isdir(path):
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

    @staticmethod
    def decode(header):
        """
        Decode RFC2047 encoded headers to Unicode.
        """
        if not header:
            return u""

        result = u""

        try:
            header_parts = decode_header(header)
        except HeaderParseError:
            return u"<En-tête corrompu>"

        for data, charset in header_parts:
            if charset is None:
                charset = "ascii"

            try:
                result += data.decode(charset, 'replace')
            except LookupError:
                result += data.decode('utf-8', 'replace')

        return result

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
        msg_subject = self.decode(message['Subject'])
        msg_from = self.decode(message['From'])
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
