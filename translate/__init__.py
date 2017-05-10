# -*- coding: utf-8 -*-

from pipobot.lib.modules import SyncModule, defaultcmd, answercmd

from translate.translate import translate


class CmdTranslate(SyncModule):
    def __init__(self, bot):
        desc = _('translate <src> <dst> <txt>: ask reverso.net to translate <txt> from <src> to <dst>')
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name='translate')

    @answercmd(r'(?P<src>[^ ]+) (?P<dst>[^ ]+) (?P<txt>.*)')
    def translate(self, sender, src, dst, txt):
        words = txt.split()
        tr = []
        for word in words:
            tr += translate(word, src, dst)
        if len(words) > 1:
            tr += translate(' '.join(words), src, dst)
        tr = list(set(tr))

        return str(tr)

    @defaultcmd
    def answer(self, sender, message):
        return self.desc
