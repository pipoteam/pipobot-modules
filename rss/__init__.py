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
                              delay=300)
        self.manager.update(silent=True)
        self._mute = False

    def action(self):
        self.manager.update(self._mute)

    @answercmd("")
    def answer(self, sender):
        return self.desc

    @answercmd(r"disable (?P<feed_name>[^ ]+)")
    def feed_disable(self, sender, feed_name):
        if self.manager.mute(feed_name):
            return u"%s désactivé avec succès" % feed_name
        else:
            return u"Aucun flux %s" % feed_name

    @answercmd(r"enable (?P<feed_name>[^ ]+)")
    def feed_enable(self, sender, feed_name):
        if self.manager.enable(feed_name):
            return u"%s activé avec succès" % feed_name
        else:
            return u"Aucun flux %s" % feed_name

    @answercmd(r"twitter add (?P<entry>[^ ]+)")
    def add_twitter(self, sender, entry):
        if self.manager.add_feed(entry, entry, twitter=True):
            return u"Flux twitter suivi avec succès"
        else:
            return u"Erreur lors de l'ajout du flux twitter %s" % entry


    @answercmd(r"add (?P<entry>[^ ]+) (?P<url>http[s]?://(?:[a-zA-Z]|[0-9]|[$-/_=?:;]|[!*\(\),~@]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)")
    def add(self, sender, entry, url):
        if self.manager.add_feed(url, entry):
            return u"Flux ajouté avec succès"
        else:
            return u"Erreur lors de l'ajout du flux : il existe déjà !!!"

    @answercmd("(remove|rm|del|delete) (?P<feed_name>[^ ]+)")
    def remove(self, sender, feed_name):
        if self.manager.rm_feed(feed_name):
            return u"Flux supprimé avec succès"
        else:
            return u"Erreur lors de la suppression du flux : il n'existe pas !!!"

    @answercmd("list")
    def list(self, sender):
        all_feeds = self.manager.list_all()
        if all_feeds == []:
            return u"Aucun flux"
        else:
            return "\n".join(map(unicode, all_feeds))
