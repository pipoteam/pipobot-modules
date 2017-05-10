# -*- coding: utf-8 -*-

from pipobot.lib.modules import SyncModule, defaultcmd

from quote.quote import quote


class CmdQuote(SyncModule):
    def __init__(self, bot):
        desc = _('quote <txt>: find a quote with <txt> on reverso.net')
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name='quote')

    @defaultcmd
    def answer(self, sender, message):
        return quote(message)
