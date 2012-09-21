#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import time
from pipobot.lib.abstract_modules import NotifyModule
from pipobot.lib.modules import answercmd
from manager import Manager
from model import Feed


class RSSNotifier(NotifyModule):
    _config = (("db_path", str, "sqlite:///rss.sqlite3"),)

    def __init__(self, bot):
        desc = {"": "Gestion de flux RSS",
                "add": "rss add [nom] [url] : abonnement à un flux RSS.",
                "remove": "rss remove [nom] : supprime totalement un flux RSS.",
                "(dis/en)able [flux]": "active/désactive un flux",
                "(un)mute": "affiche/n'affiche plus les nouvelles entrées RSS",
                "list": "rss list : affiche tous les flux RSS"
                }

        self.manager = Manager(self.db_path, bot)
        NotifyModule.__init__(self,
                              bot,
                              command="rss",
                              desc=desc,
                              delay=60)
        self.manager.update(silent=True)
        self.mute = False

    def action(self):
        self.manager.update(self.mute)

    @answercmd("^$")
    def answer(self, sender, message):
        return self.desc

    @answercmd(r"disable ([^ ]+)")
    def feed_disable(self, sender, message):
        feed_name = message.group(1)
        if self.manager.mute(feed_name):
            return u"%s désactivé avec succès" % feed_name
        else:
            return u"Aucun flux %s" % feed_name

    @answercmd(r"enable ([^ ]+)")
    def feed_enable(self, sender, message):
        feed_name = message.group(1)
        if self.manager.enable(feed_name):
            return u"%s activé avec succès" % feed_name
        else:
            return u"Aucun flux %s" % feed_name

    @answercmd(r"add ([^ ]+) (http[s]?://(?:[a-zA-Z]|[0-9]|[$-/_=?:;]|[!*\(\),~@]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)")
    def add(self, sender, message):
        entry = message.group(1)
        url = message.group(2)
        if self.manager.add_feed(url, entry):
            return u"Flux ajouté avec succès"
        else:
            return u"Erreur lors de l'ajout du flux : il existe déjà !!!"

    @answercmd("remove ([^ ]+)", "delete ([^ ]+)", "rm ([^ ]+)", "del ([^ ]+)")
    def remove(self, sender, message):
        feed_name = message.group(1)
        if self.manager.rm_feed(feed_name):
            return u"Flux supprimé avec succès"
        else:
            return u"Erreur lors de la suppression du flux : il n'existe pas !!!"

    @answercmd("list")
    def list(self, sender, args):
        all_feeds = self.manager.list_all()
        if all_feeds == []:
            return u"Aucun flux"
        else:
            return "\n".join(map(unicode, all_feeds))
