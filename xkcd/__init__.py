# -*- coding: utf-8 -*-

from json import loads

from pipobot.lib.abstract_modules import FortuneModule
from pipobot.lib.module_test import ModuleTest


class CmdXKCD(FortuneModule):
    def __init__(self, bot):
        desc = 'Pour afficher des XKCD.'
        desc += '\nxkcd: Affiche un xkcd aléatoire.'
        desc += '\nxkcd <n>: Affiche le xkcd <n>'
        FortuneModule.__init__(self,
                               bot,
                               desc=desc,
                               name="xkcd",
                               url_random="https://xkcd.com/221/info.0.json",
                               url_indexed="https://xkcd.com/%s/info.0.json",
                               lock_time=2,
                               )

    def extract_data(self, html_content):
        data = loads(html_content)
        ret = u"Mandatory XKCD: {title} -- https://xkcd.com/{num}/ ({day}/{month}/{year})".format(data)
        return {
            'text': ret,
            'xhtml': u'<a href="https://xkcd.com/%i"><img alt="%s" src="%s" /></a>' % (data['num'], ret, data['img']),
        }


class XKCDTest(ModuleTest):
    def test_random(self):
        ret = 'Mandatory XKCD: Random Number -- https://xkcd.com/221/ (9/2/2007)'
        self.assertEqual(self.bot_answer("!xkcd"), ret)

    def test_ok(self):
        ret = 'Mandatory XKCD: Voting Software -- https://xkcd.com/2030/ (8/8/2018)'
        self.assertEqual(self.bot_answer('!xkcd 2030'), ret)
