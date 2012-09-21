#!/usr/bin/python
# -*- coding: UTF-8 -*-
import libcanal
import config
from pipobot.lib.modules import defaultcmd, answercmd
from pipobot.lib.abstract_modules import NotifyModule

DEFAULT_TIMER = 60


class CmdCanalPlus(NotifyModule):
    _config = (("timer", int, DEFAULT_TIMER), ("notify", list, []))

    def __init__(self, bot):
        desc = """Pour récuperer des url de vidéos sur canalplus
!canal emission : donne les liens rtmp pour l'emission dans toutes les qualités
!canal emission [HD|BAS_DEBIT|HAUT_DEBIT] : donne le lien pour la qualité spécifiée
!canal mute/unmute : désactive/active les notifications """

        NotifyModule.__init__(self,
                              bot,
                              desc=desc,
                              command="canal",
                              delay=self.timer)
        self.shows = {}
        for show in config.emissions_id.keys():
            em = libcanal.Emission(show, notif=(show in self.notify))
            em.update()
            self.shows[show] = em

    @defaultcmd
    def answer(self, sender, message):
        if message == "":
            return u"usage : !canal emission [quality], avec emission parmi %s" % ", ".join(config.emissions_id.keys())
        emission = message
        args = emission.split()
        name = args[0]
        if name in self.shows:
            show = self.shows[name]
            if self.mute:
                show.update()
        else:
            try:
                show = libcanal.Emission(name)
                self.shows[name] = show
            except libcanal.UnknownEmission:
                return u"Je ne connais pas l'émission %s" % name

        if len(args) > 1:
            quality = args[1]
            try:
                url = show.last_vid.get_url(quality)
                vid = show.last_vid
                return u"%s - %s\n%s : %s" % (vid.title, vid.subtitle, quality, url)
            except libcanal.QualityException:
                return u"La vidéo %s n'existe pas avec cette qualité (%s)" % (name, quality)
        res = {}
        vid = show.last_vid
        vid_data = u"%s - %s" % (vid.title, vid.subtitle)
        return "\n".join([vid_data] + ["%s : %s" % (quality, link) for quality, link in vid.links.iteritems()])

    def do_action(self):
        for show in [elt for elt in self.shows.values() if elt.notif]:
            updated = show.update()
            if updated:
                url = show.last_vid.get_url("HD")
                msg = u"Nouvel épisode de %s !!!\n" % show.name
                msg += u"Lien HD : %s" % str(url)
                self.bot.say(">> %s" % msg)

    def update(self, silent=False):
        for show in self.shows.values():
            updated = show.update()
