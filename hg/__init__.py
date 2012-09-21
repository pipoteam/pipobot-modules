#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import yaml
import hglib
import mercurial
from pipobot.lib.modules import SyncModule, answercmd
from pipobot.lib.exceptions import ConfigException


class CmdHg(SyncModule):
    _config = (("default", str, ""), ("repos", dict, {}))

    def __init__(self, bot):
        desc = """hg : donne le dernier changement sur le repo %s
hg [repo] : donne le dernier changement du repo [repo]
hg [repo] [rev] : affiche la révision [rev] du repo [repo]""" % (self.default)
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            command="hg")

    @answercmd(r"^$")
    def answer_default(self, sender, message):
        repo = self.default
        return self.get_log(repo, -1)

    @answercmd(r"^(?P<name>\w+)$")
    def answer_repo(self, sender, message):
        repo = message.group("name")
        if repo == "repos":
            return "Liste des repos connus : %s" % (", ".join(self.repos))
        return self.get_log(repo, -1)

    @answercmd(r"^(?P<name>\w+)\s+(?P<rev>\d+)$")
    def answer_repo_rev(self, sender, message):
        repo = message.group("name")
        rev = message.group("rev")
        return self.get_log(repo, rev)

    def get_log(self, repo, rev):
        if not repo in self.repos:
            return "Le repo %s n'existe pas" % repo
        try:
            return hglib.log(self.repos[repo], int(rev))
        except mercurial.error.RepoError:
            return "Le répertoire %s associé à %s n'est pas valide !" % (self.repos[repo], repo)
