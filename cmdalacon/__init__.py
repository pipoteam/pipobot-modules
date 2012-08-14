#! /usr/bin/env python
#-*- coding: utf-8 -*-
import ConfigParser
import logging
import os
import random
import re
from pipobot.lib.modules import MultiSyncModule, defaultcmd

def multiwordReplace(text, wordDic):
    """
    take a text and replace words that match a key in a dictionary with
    the associated value, return the changed text
    """
    rc = re.compile('|'.join(map(re.escape, wordDic)))
    def translate(match):
        return wordDic[match.group(0)]
    return rc.sub(translate, text)


class ListConfigParser(ConfigParser.RawConfigParser):
    def get(self, section, option):
        "Redéfinition du get pour gérer les listes"
        value = ConfigParser.RawConfigParser.get(self, section, option)
        if (value[0] == "[") and (value[-1] == "]"):
            return eval(value)
        else:
            return value

    def set(self, section, option, value):
        if option == 'desc':
            ConfigParser.RawConfigParser.set(self, section, option, value)
        else:
            old = ConfigParser.RawConfigParser.get(self, section, option)
            if (old[0] == "[") and (old[-1] == "]"):
                ConfigParser.RawConfigParser.set(self, section, option, '%s, "%s"]' % (old[:-1], value))
            else:
                ConfigParser.RawConfigParser.set(self, section, option, '["%s", "%s"]' % (old, value))


class CmdAlacon(MultiSyncModule):
    def __init__(self, bot):
        settings = bot.settings
        self.config = ''
        self.config_path = ''
        try:
            self.config_path = settings['modules']['cmdalacon']['config_path']
        except KeyError:
            config_dir = bot.module_path["cmdalacon"]
            self.config_path = os.path.join(config_dir, "cmdlist.cfg")
        commands = self.readconf(bot)
        MultiSyncModule.__init__(self,
                        bot,
                        commands=commands)


    def extract_to(self, cmd, value, backup):
        try:
            v = self.config.get(cmd, value)
        except ConfigParser.NoOptionError :
            v = self.config.get(cmd, backup)
        if type(v) != list:
            v = [v]
        self.dico[cmd][value] = v

    def readconf(self, bot):
        #name, description and actions associated to each command
        self.dico = {}
        #To initialize MultiSyncModule
        commands = {}

        self.config = ListConfigParser()
        self.config.read(self.config_path)
        for c in self.config.sections() :
            self.dico[c] = {}
            self.dico[c]['desc'] = self.config.get(c, 'desc')
            commands[c] = self.dico[c]['desc']
            self.dico[c]['toNobody'] = self.config.get(c, 'toNobody') if type(self.config.get(c, 'toNobody')) == list else [self.config.get(c, 'toNobody')]
            self.extract_to(c, "toSender", "toNobody")
            self.extract_to(c, "toBot", "toNobody")
            self.extract_to(c, "toSomebody", "toNobody")
        return commands

    def addtoconf(self, cmd, desc, toNobody, toSender='', toBot='', toSomebody=''):
        if cmd not in self.config.sections():
            #TODO: check for conflicts
            ConfigParser.RawConfigParser.add_section(self, section)
        self.config.set(cmd, 'desc', desc)
        self.config.set(cmd, 'toNobody', toNobody)
        self.config.set(cmd, 'toSender', toSender)
        self.config.set(cmd, 'toBot', toBot)
        self.config.set(cmd, 'toSomebody', toSomebody)
        with open(self.config_path, 'wb') as configfile:
            self.config.write(configfile)

    @defaultcmd
    def answer(self, cmd, sender, message):
        toall = self.bot.occupants.get_all(" ", [self.bot.name, sender])
        replacement = {"__somebody__" : message, "__sender__" : sender, "_all_" : toall}
        if message.lower() == sender.lower():
            key = "toSender"
        elif message == '':
            key = "toNobody"
        elif message.lower() == self.bot.name.lower():
            key = "toBot"
        else:
            key = "toSomebody"
        return multiwordReplace(multiwordReplace(random.choice(self.dico[cmd][key]), replacement), replacement)
