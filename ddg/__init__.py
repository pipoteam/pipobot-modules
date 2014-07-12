#!/usr/bin/env python
#-*- coding: utf8 -*-
from bs4 import BeautifulSoup, Tag
import urllib.request, urllib.parse, urllib.error
import duckduckgo
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.utils import xhtml2text

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
        for result in rep.related[:MAX_RESULT]:
            if hasattr(result, "text"):
                res.append("%s - %s" % (result.text, result.url))
            else:
                res.append("%s - %s" % (result.topics[0].text,
                                        result.topics[0].url))
        return "\n".join(res)
    # If the API does not have return any usefull result, we do a real search in ddg
    return html_request(msg)


def html_request(msg):
    site = urllib.request.urlopen('http://duckduckgo.com/html/?q=%s' % msg)
    data = site.read()
    soup = BeautifulSoup(data)
    site.close()

    links = soup.findAll('div', {'class': "links_main links_deep"})
    results = ""
    for link in links[:MAX_RESULT]:
        url = link.find("a").get("href")
        contents = link.find("a").contents
        title = ""
        for data in contents:
            if isinstance(data, Tag):
                title += " %s" % data.getString()
            else:
                title += " %s" % str(xhtml2text(data))
        results += "%s - %s\n" % (title.strip(), url)

    return results.strip()

class CmdDDG(SyncModule):
    def __init__(self, bot):
        desc = "!ddg mot-clé : recherche dans duckduckgo"
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="ddg")

    @defaultcmd
    def answer(self, sender, message):
        if message == '':
            return self.desc
        else:
            return ddg_request(message)
