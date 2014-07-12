#! /usr/bin/python
# -*- coding: utf-8 -*-
from time import time
from pipobot.lib.modules import SyncModule, defaultcmd, answercmd
from .parser import extract


CACHE_TIME = 3600


class CmdTv(SyncModule):
    def __init__(self, bot):
        desc = {"": "Donne les programmes tv de la soirée",
                "!tv channels": "Affiche la liste des chaînes disponibles",
                "!tv <une_chaine>": "Donne les programmes de la soirée pour une chaîne"}
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="tv")
        self.cache = None
        self.cache_time = None

    def _get_data(self):
        if self.cache_time is None or time() - self.cache_time > CACHE_TIME:
            res = extract()
            self.cache = res
            self.cache_time = time()
        else:
            res = self.cache
        return res

    @answercmd("channels")
    def channels(self, sender):
        data = self._get_data()
        return "Les chaînes valides sont les suivantes :\n%s" % \
                (", ".join(sorted(self._get_data().keys())))

    @defaultcmd
    def answer(self, sender, message):
        args = message.strip()
        res = self._get_data()

        if args == "":
            channels = ("tf1", "france 2", "france 3", "canal+", "arte", "m6")
            return "\n".join("%s : %s" % (key, res[key]) for key in channels)
        else:
            try:
                return "%s : %s" % (args, res[args.lower()])
            except KeyError:
                return "%s n'est pas une chaîne valide... Regardez le help pour plus d'informations" % args
