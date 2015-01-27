# -*- coding: utf-8 -*-

from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.utils import check_url


class Gags(SyncModule):
    def __init__(self, bot):
        desc = _('retrieves a random 9gag page.')
        SyncModule.__init__(self,
                                 bot,
                                 desc=desc,
                                 name="9gag")

    @defaultcmd
    def answer(self, sender, message):
        return check_url('http://9gag.com/random', geturl=True)
