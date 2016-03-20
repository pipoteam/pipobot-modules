# -*- coding: utf-8 -*-

import requests
from pipobot.lib.modules import SyncModule, answercmd, defaultcmd

from .model import KickStart


class CmdKickStarter(SyncModule):
    def __init__(self, bot):
        desc = _("kickstarter : show this help\n")
        desc += _("kickstarter list: list known projects\n")
        desc += _("kickstarter all: show the status of all known projects\n")
        desc += _("kickstarter add <project-owner>/<project-name>: add a project\n")
        desc += _("kickstarter rm <project-name>: remove a project\n")
        desc += _("kickstarter <project-name>: show the status of the project")
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="kickstarter")

    @answercmd(r'^add (?P<owner>[^/]+)/(?P<name>[^/]+)')
    def answer_add(self, sender, owner, name):
        k = KickStart(name=name, owner=owner)
        if requests.get(k.url()).status_code != 200:
            return _("'%s' is not reachable" % k.url())
        self.bot.session.add(k)
        self.bot.session.commit()
        return _("Kickstarter's projetct '%s' has correctly been added" % name)

    @answercmd(r'^rm (?P<name>\S+)')
    def answer_rm(self, sender, name):
        k = self.bot.session.query(KickStart).filter(KickStart.name == name).first()
        if not k:
            return _("I can't find project '%s'..." % name)
        owner = k.owner
        self.bot.session.delete(k)
        self.bot.session.commit()
        return _("Project '%s/%s' removed" % (owner, name))

    @answercmd(r'^list')
    def answer_list(self, sender):
        ret = _("Currently known kickstarter's projects:\n")
        return ret + "\n".join([k.name for k in self.bot.session.query(KickStart).all()])

    @answercmd(r'^all')
    def answer_all(self, sender):
        ret = _("Currently known kickstarter's projects:\n")
        return ret + "\n".join([k.status() for k in self.bot.session.query(KickStart).all()])

    @answercmd(r'^(?P<name>\S+)')
    def answer_user(self, sender, name):
        k = self.bot.session.query(KickStart).filter(KickStart.name == name).first()
        if k:
            return k.status()
        return _("I don't know the project %s..." % name)

    @defaultcmd
    def answer_default(self, sender, message):
        return self.desc
