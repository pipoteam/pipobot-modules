#-*- coding: utf8 -*-
import requests
import pipobot.lib.utils
from pipobot.lib.modules import SyncModule, defaultcmd
from pipobot.lib.module_test import ModuleTest


class CmdGoogle(SyncModule):
    def __init__(self, bot):
        desc = "!google mot-clé : recherche le mot clé dans google"
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="google")

    @defaultcmd
    def answer(self, sender, message):
        if message == '':
            return self.desc
        else:
            url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0'
            req = requests.get(url, params={"q": message})
            json = req.json()
            results = json['responseData']['results']

            ans = ''
            ans_xhtml = ''
            for i in results:
                ans += '\n' + i['url'] + ' --- ' + i['title']
                ans_xhtml += '<br/>\n<a href="' + i['url'] + '" >' + i['title'] + '</a>'
                ans_xhtml = ans_xhtml.replace("b>", "strong>")
            rep = {}
            rep["text"] = pipobot.lib.utils.xhtml2text(ans)
            rep["xhtml"] = ans_xhtml
            return rep


class GoogleTest(ModuleTest):
    def test_google(self):
        self.bot_answer("!google test")
