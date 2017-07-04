#-*- coding: utf-8 -*-
from . import core
from pipobot.lib.modules import MultiSyncModule, defaultcmd
from pipobot.lib.module_test import ModuleTest


class CmdNextPrev(MultiSyncModule):
    def __init__(self, bot):
        names = {"next": "next [show1;show2;show3]\nAffiche les infos sur le prochain épisode en date de show1,show2,show3",
                    "prev": "prev [show1;show2;show3]\nAffiche les infos sur le dernier épisode en date de show1,show2,show3"}
        MultiSyncModule.__init__(self,
                                 bot,
                                 names=names)

    @defaultcmd
    def answer(self, cmd, sender, message):
        return core.getdata(message, cmd=="next")
