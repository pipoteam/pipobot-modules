# -*- coding: utf-8 -*-
import ConfigParser
import os

from pipobot.lib.modules import MultiSyncModule, defaultcmd
from pipobot.lib.utils import check_url

DEFAULT_CONFIG = os.path.join(os.path.dirname(__file__), "urllist.cfg")


class Link(MultiSyncModule):
    _config = (("config_path", str, DEFAULT_CONFIG),)

    def __init__(self, bot):
        names = self.readconf(bot)
        MultiSyncModule.__init__(self,
                                 bot,
                                 names=names)

    def readconf(self, bot):
        # name, description and url associated to each link
        self.dico = {}
        names = {}

        config = ConfigParser.RawConfigParser()
        config.read(self.config_path)
        for c in config.sections():
            self.dico[c] = {}
            self.dico[c]['desc'] = config.get(c, 'desc')
            names[c] = self.dico[c]['desc']
            self.dico[c]['url'] = config.get(c, 'url')
        return names

    @defaultcmd
    def answer(self, cmd, sender, message):
        url = self.dico[cmd]['url']
        if message:
            if 'KEYWORDS' in url:
                url = url.replace('KEYWORDS', message).replace(' ', '+')
            else:
                return _("This command does not take arguments")
        return check_url(url.encode('utf-8'), geturl=True)
