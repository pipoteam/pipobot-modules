#! /usr/bin/env python
#-*- coding: utf-8 -*-

import os
import re
import random
import logging
import ConfigParser
from model import CmdAlacons, AnswersAlacon
from pipobot.lib.modules import MultiSyncModule, defaultcmd, answercmd

def multiwordReplace(text, wordDic):
    """
    take a text and replace words that match a key in a dictionary with
    the associated value, return the changed text
    """
    rc = re.compile('|'.join(map(re.escape, wordDic)))
    def translate(match):
        return wordDic[match.group(0)]
    return rc.sub(translate, text)

def anstostr(ansto):
    if ansto == 1:
        return 'toSender'
    elif ansto == 2:
        return 'toNobody'
    elif ansto == 3:
        return 'toBot'
    elif ansto == 4:
        return 'toSomebody'
    elif ansto == 5:
        return 'toSomething'
    return 'Unknown ansto…'

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
            try:
                old = ConfigParser.RawConfigParser.get(self, section, option)
                if (old[0] == "[") and (old[-1] == "]"):
                    ConfigParser.RawConfigParser.set(self, section, option, '%s, "%s"]' % (old[:-1], value))
                else:
                    ConfigParser.RawConfigParser.set(self, section, option, '["%s", "%s"]' % (old, value))
            except ConfigParser.NoOptionError:
                ConfigParser.RawConfigParser.set(self, section, option, '["%s"]' % value)


class CmdAlacon(MultiSyncModule):
    def __init__(self, bot):
        self.config = ''
        self.config_path = ''
        try:
            self.config_path = bot.settings['modules']['cmdalacon']['config_path']
        except KeyError:
            config_dir = bot.module_path["cmdalacon"]
            self.config_path = os.path.join(config_dir, "cmdlist.cfg")

        self.bot = bot
        self.commands = self.readdb()
        MultiSyncModule.__init__(self,
                bot,
                commands=self.commands)  # TODO: __init__ again ?

    def extract_to(self, cmd, value, backup):
        try:
            v = self.config.get(cmd, value)
        except ConfigParser.NoOptionError :
            v = self.config.get(cmd, backup)
        if type(v) != list:
            v = [v]
        self.dico[cmd][value] = v

    def readdb(self):
        commands = {}
        print type(self), '−−−−', self
        print type(self.bot), '−−−−', self.bot
        print type(self.bot.session), '−−−−', self.bot.session
        print type(self.bot.session.query(CmdAlacons)), '−−−−', self.bot.session.query(CmdAlacons)
        print type(self.bot.session.query(CmdAlacons).all()), '−−−−', self.bot.session.query(CmdAlacons).all()
        commandes = self.bot.session.query(CmdAlacons).all()
        print commandes
        for cmd in commandes:
            self.dico[cmd] = {}
            self.dico[cmd]['desc'] = cmd.desc
            commands[cmd] = cmd.desc
            for ans in cmd.answers:
                ansto = anstostr(ans.ansto)
                if not self.dico[cmd][anstostr]:
                    self.dico[cmd][anstostr] = []
                self.dico[cmd][anstostr].append(answer)
        return commands

    @answercmd(r'^readconfig')
    def readconf(self, sender, message):  # TODO check rights
        ret = ''
        config = ListConfigParser()
        config.read(self.config_path)
        for cmd in config.sections() :
            desc = self.config.get(cmd, 'desc')
            if cmd not in self.commands:
                newcmd = CmdAlacons(cmd, desc)
                self.bot.session.add(newcmd)
                self.bot.session.commit()
                self.dico[cmd] = {}
                ret += 'cmd "%s: %s" added, ' % (cmd, desc)
            cmdentry = self.bot.session.query(CmdAlacons).filter(CmdAlacons.cmd == cmd).first()
            if cmdentry.desc != desc:
                cmdentry.desc = desc
                self.bot.session.commit()
                ret += 'cmd %s\'s desc set to "%s", ' % (cmd, desc)

            for section in range(1,6):
                answers = None
                anstostr = anstosto(section)
                try:
                    answers = self.config.get(cmd, anstostr)
                except ConfigParser.NoOptionError:
                    continue
                if type(answers) != list:
                    v = [answers]
                for answer in answers:
                    if answer not in self.dico[cmd][anstostr]:
                        newanswer = AnswersAlacon(cmdentry.cmid, answer, section)
                        self.bot.session.add(newanswer)
                        self.bot.session.commit()
                        if not self.dico[cmd][anstostr]:
                            self.dico[cmd][anstostr] = []
                        self.dico[cmd][anstostr].append(answer)
                        ret +='answer "%s" added to cmd %s: %s' % (answer, cmd, anstostr)
            #TODO: check que y’a un toNobody
        return ret

    @answercmd(r'^writeconfig')
    def writeconf(self, sender, message):  # TODO check rights
        config = ListConfigParser()
        for cmd in self.dico:
            config.add_section(cmd)
            config.set(cmd, 'desc', self.dico[cmd]['desc'])
            for section in range(1, 6):
                config.set(cmd, anstostr(section), self.dico[cmd][anstostr(section)])

        with open(self.config_path + '.new', 'wb') as configfile:
            config.write(configfile)

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
        if cmd == 'readconf':
            return self.readconf()
        if cmd == 'writeconf':
            return self.writeconf()

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
