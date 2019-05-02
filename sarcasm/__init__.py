# -*- coding: utf-8 -*-

import random

from pipobot.lib.modules import SyncModule, defaultcmd


class CmdSarcasm(SyncModule):
    def __init__(self, bot):
        desc = _('Sarcasm <message>: sarcasmify your <message>')
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name='sarcasm')

    @defaultcmd
    def answer(self, sender, message):
        return ''.join(c.upper() if random.getrandbits(1) else c.lower() for c in message)
