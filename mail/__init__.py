#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
from pipobot.lib.modules import AsyncModule
import mbox
import mdir

logger = logging.getLogger("mail")


class Mail(AsyncModule):
    """A module for notification of emails"""

    def __init__(self, bot):
        AsyncModule.__init__(self,
                             bot,
                             name="mail",
                             desc="Displaying incoming mails",
                             delay=0)

        if hasattr(self.__class__, '_settings'):
            box_format = self._settings['format']
            if box_format == "mbox":
                try:
                    box_path = self._settings["path"]
                except KeyError:
                    #~/Maildir will be used
                    box_path = ""
                self.notifier = mbox.MboxNotify(bot, box_path)
            elif box_format == "mdir":
                try:
                    box_path = self._settings["path"]
                except KeyError:
                    box_path = ""
                self.notifier = mdir.MdirNotify(bot, box_path)
            else:
                logger.error(u"Mail box format %s not defined. You must use either mbox or mdir !" % box_format)
        else:
            self.delay = 60
            logger.error(u"You must specify a mailbox format in your configuration file")

    def action(self):
        if hasattr(self, "notifier"):
            self.notifier.action()
