# -*- coding: utf-8 -*-

from pipobot.lib.modules import SyncModule, defaultcmd


class CmdDoge(SyncModule):
    def __init__(self, bot):
        desc = _('doge <message>: dogifies your <message>')
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name='doge')

    @defaultcmd
    def answer(self, sender, message):
        if len(message.split(',')) == 2:
            such, very = message.split(',')
        elif len(message.split()) == 2:
            such, very = message.split()
        else:
            such, very = message, 'amazing'
        return 'Such %s!\nVery %s!Wow !' % (such, very)
