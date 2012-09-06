#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
from pipobot.lib.modules import AsyncModule
import mbox
import mdir

logger = logging.getLogger("mail")


class Mail(AsyncModule):
    """A module for notification of emails"""
    _config = (("format", str, None), ("path", str, ""))

    def __init__(self, bot):
        AsyncModule.__init__(self,
                             bot,
                             name="mail",
                             desc="Displaying incoming mails",
                             delay=0)

        if self.format == "mbox":
            self.notifier = mbox.MboxNotify(bot, self.path)
        elif self.format == "mdir":
            self.notifier = mdir.MdirNotify(bot, self.path)
        elif self.format != "":
            self.alive = False
            logger.error(u"Mail box format « %s » not defined. You must use either mbox or mdir !" % self.format)
        elif self.format == "":
            self.delay = 10

    def action(self):
        if hasattr(self, "notifier"):
            self.notifier.action()
