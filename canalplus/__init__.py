#!/usr/bin/python
# -*- coding: UTF-8 -*-
from . import libcanal
import logging
import traceback
from . import config
from pipobot.lib.modules import defaultcmd
from pipobot.lib.abstract_modules import NotifyModule

DEFAULT_TIMER = 60
logger = logging.getLogger("Canalplus module")

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
                              name="canal",
                              delay=self.timer)
        self.shows = {}
        for show in list(config.emissions_id.keys()):
            try:
                em = libcanal.Emission(show, notif=(show in self.notify))
                em.update()
                self.shows[show] = em
            except:
                logger.error("Error loading show %s : %s" % (show, traceback.format_exc()))

    @defaultcmd
    def answer(self, sender, message):
        if message == "":
            return "usage : !canal emission [quality], avec emission parmi %s" % ", ".join(list(config.emissions_id.keys()))
        emission = message
        args = emission.split()
        name = args[0]
        if name in self.shows:
            show = self.shows[name]
            if self._mute:
                show.update()
        else:
            try:
                show = libcanal.Emission(name)
                self.shows[name] = show
            except libcanal.UnknownEmission:
                return "Je ne connais pas l'émission %s" % name
            except:
                logger.error("Error loading show %s : %s" % (name, traceback.format_exc()))
                return "L'émission %s n'est pas disponible" % name

        if len(args) > 1:
            quality = args[1]
            try:
                url = show.last_vid.get_url(quality)
                vid = show.last_vid
                return "%s - %s\n%s : %s" % (vid.title, vid.subtitle, quality, url)
            except libcanal.QualityException:
                return "La vidéo %s n'existe pas avec cette qualité (%s)" % (name, quality)
        res = {}
        vid = show.last_vid
        vid_data = "%s - %s" % (vid.title, vid.subtitle)
        return "\n".join([vid_data] + ["%s : %s" % (quality, link) for quality, link in vid.links.items()])

    def do_action(self):
        for show in [elt for elt in list(self.shows.values()) if elt.notif]:
            updated = show.update()
            if updated:
                url = show.last_vid.get_url("HD")
                msg = "Nouvel épisode de %s !!!\n" % show.name
                msg += "Lien HD : %s" % str(url)
                self.bot.say(">> %s" % msg)

    def update(self, silent=False):
        for show in list(self.shows.values()):
            updated = show.update()
