# -*- coding: utf-8 -*-
import json
import urllib
from pipobot.lib.modules import SyncModule, answercmd
from collections import deque

BASE_URL = "http://www.urbandictionary.com/iphone/search/define"
MAX_CACHE = 10 


class UrbanDict(SyncModule):
    def __init__(self, bot):
        desc = ("urban [result] [query] : displays the [result]-th response to the [query]\n"
                "urban : displays a random urban dictionary entry")
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="urban")
        self._cache = deque()

    def add_cache(self, request, result):
        if len(self._cache) == MAX_CACHE:
            self._cache.popleft()
        self._cache.append((request, result))

    def get_cache(self, request):
        for req, result in self._cache:
            if req == request:
                return result

    @answercmd("")
    def random_urban(self, sender):
        url = "http://www.urbandictionary.com/random.php"
        page = urllib.urlopen(url)
        content = page.read()
        page.close()
        # The random page is a redirection like this : 
        # <html><body>You are being <a href="http://www.urbandictionary.com/define.php?term=RTM">redirected</a>.</body></html>
        words = content.partition("define.php?term=")[2].partition('"')[0]
        return self.urbandict(sender, req=words, select=0)


    @answercmd("(?P<select>\d+)?(?P<req>.+)")
    def urbandict(self, sender, req=None, select=None):
        if req is None:
            return self.random_urban(sender)
        req = req.strip()
        if select is None:
            select = 0
        else:
            select = int(select)

        defs = self.get_cache(req)
        if defs is None:
            params = urllib.urlencode({"term" : req})
            page = urllib.urlopen("%s?%s" % (BASE_URL, params))
            content = page.read()
            page.close()
            urban_json = json.loads(content)
            if urban_json["result_type"] == "no_results":
                self.add_cache(req, [])
                return u"No result found"
            defs = urban_json["list"]
            self.add_cache(req, defs)
        elif defs == []:
            return u"Still no result found"

        result = ""
        if select >= len(defs):
            result += "There are only %s definitions for this query : here is the first one : \n" % len(defs)
            select = defs[0]
        else:
            select = defs[select]
        result += u"%s : %s\nExample : %s" % (select["permalink"], select["definition"], select["example"])
        return result
