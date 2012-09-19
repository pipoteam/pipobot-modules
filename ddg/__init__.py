#!/usr/bin/env python
#-*- coding: utf8 -*-
import urllib
import simplejson
from pipobot.lib.modules import SyncModule, defaultcmd
import pipobot.lib.utils

#API for duckduckgo : http://pypi.python.org/pypi/duckduckgo2
import duckduckgo

MAX_RESULT = 5


def ddg_request(msg):
    rep = duckduckgo.query(msg)
    if rep.type == "answer":
        return "%s - %s" % (rep.abstract.text, rep.abstract.url)
    elif rep.type == "nothing" or rep.type == "exclusive":
        if rep.answer.text != "":
            return rep.answer.text
    elif rep.type == "disambiguation":
        res = []
        for result in rep.related:
            if hasattr(result, "text"):
                res.append("%s - %s" % (result.text, result.url))
            else:
                res.append("%s - %s" % (result.topics[0].text,
                                        result.topics[0].url))
        return "\n".join(res[:MAX_RESULT])
    return u"Aucun résultat intéressant"


class CmdDDG(SyncModule):
    def __init__(self, bot):
        desc = u"!ddg mot-clé : recherche dans duckduckgo"
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            command="ddg")

    @defaultcmd
    def answer(self, sender, message):
        if message == '':
            return self.desc
        else:
            return ddg_request(message)
