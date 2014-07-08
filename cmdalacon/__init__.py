#-*- coding: utf-8 -*-
import configparser
import os
import random
import re
from pipobot.lib.modules import MultiSyncModule, defaultcmd
from pipobot.lib.known_users import KnownUser

DEFAULT_CONFIG = os.path.join(os.path.dirname(__file__), "cmdlist.cfg")


def multiwordReplace(text, wordDic):
    """
    take a text and replace words that match a key in a dictionary with
    the associated value, return the changed text
    """
    rc = re.compile('|'.join(map(re.escape, wordDic)))

    def translate(match):
        return wordDic[match.group(0)]
    return rc.sub(translate, text)


class ListConfigParser(configparser.RawConfigParser):
    def get(self, section, option):
        "Redéfinition du get pour gérer les listes"
        value = configparser.RawConfigParser.get(self, section, option)
        if (value[0] == "[") and (value[-1] == "]"):
            return eval(value)
        else:
            return value


class CmdAlacon(MultiSyncModule):
    _config = (("config_path", str, DEFAULT_CONFIG),)

    def __init__(self, bot):
        names = self.readconf(bot)
        MultiSyncModule.__init__(self,
                                 bot,
                                 names=names)

    def extract_to(self, config, cmd, value, backup):
        try:
            v = config.get(cmd, value)
        except configparser.NoOptionError:
            v = backup
        if type(v) is not list:
            v = [v]
        self.dico[cmd][value] = v

    def readconf(self, bot):
        # name, description and actions associated to each command
        self.dico = {}
        # To initialize MultiSyncModule
        names = {}

        config = ListConfigParser()
        config.read(self.config_path)

        for command_name in config.sections():
            self.dico[command_name] = {}
            self.dico[command_name]['desc'] = config.get(command_name, 'desc')
            names[command_name] = self.dico[command_name]['desc']

            nobody = config.get(command_name, "toNobody")
            for key in ("toNobody", "toSender", "toBot", "toSomebody"):
                self.extract_to(config, command_name, key, nobody)
        return names

    @defaultcmd
    def answer(self, cmd, sender, message):
        toall = KnownUser.get_all(self.bot, " ", [self.bot.name, sender])
        replacement = {"__somebody__": message, "__sender__": sender, "_all_": toall}
        if message.lower() == sender.lower():
            key = "toSender"
        elif message == '':
            key = "toNobody"
        elif message.lower() == self.bot.name.lower():
            key = "toBot"
        else:
            key = "toSomebody"
        return multiwordReplace(multiwordReplace(random.choice(self.dico[cmd][key]), replacement), replacement)
