#! /usr/bin/env python
#-*- coding: utf-8 -*-
import os
import ConfigParser
from pipobot.lib.modules import MultiSyncModule, defaultcmd
from pipobot.lib.url import check_url


class Link(MultiSyncModule):
    def __init__(self, bot):
        commands = self.readconf(bot)
        MultiSyncModule.__init__(self,
                        bot,
                        commands=commands)

    def readconf(self, bot):
        #name, description and url associated to each link
        self.dico = {}
        commands = {}

        settings = bot.settings
        config_path = ''
        try:
            config_path = settings['modules']['link']['config_path']
        except KeyError:
            config_dir = bot.module_path["link"]
            config_path = os.path.join(config_dir, "urllist.cfg")

        config = ConfigParser.RawConfigParser()
        config.read(config_path)
        for c in config.sections():
            self.dico[c] = {}
            self.dico[c]['desc'] = config.get(c, 'desc')
            commands[c] = self.dico[c]['desc']
            self.dico[c]['url'] = config.get(c, 'url')
        return commands

    @defaultcmd
    def answer(self, cmd, sender, message):
        if message:
            return check_url(self.dico[cmd]['url'].replace('KEYWORDS', message).replace(' ', '+'), geturl=True)
        return "rtfm ;)"
