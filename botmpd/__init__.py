#! /usr/bin/python2
# -*- coding: utf-8 -*-

import logging
from mpd import ConnectionError
import pipobot.lib.exceptions
from pipobot.lib.modules import defaultcmd, answercmd
from pipobot.lib.abstract_modules import NotifyModule
from .libmpd.BotMPD import BotMPD


logger = logging.getLogger("pipobot.botmpd")


class CmdMpd(NotifyModule):
    _config = (("host", str, "localhost"),
               ("port", int, 6600),
               ("pwd", str, None),
               ("datadir", str, ""))

    def __init__(self, bot):
        desc = {"": "Controle du mpd",
                "current": "mpd current : chanson actuelle",
                "next": "mpd next : chanson suivante",
                "prev": "mpd prev : chanson précédente",
                "shuffle": "mpd shuffle : fait un shuffle sur la playlist",
                "list": "mpd list [n] : liste les [n] chansons suivantes",
                "clear": "mpd clear : vide la playlist (ou pas)",
                "search": "mpd search (Artist|Title) requete : cherche toutes les pistes d'Artiste/Titre correspondant à la requête",
                "setnext": "mpd setnext [i] : place la chanson à la position [i] dans la playlist après la chanson courante (enfin elle court pas vraiment)",
                "nightmare": "mpd nightmare [i] : les [i] prochaines chansons vont vous faire souffrir (plus que le reste)",
                "clean": "mpd clean : pour retarder l'inévitable...",
                "settag": "mpd settag [artist|title]=Nouvelle valeur",
                "lyrics": "mpd lyrics: permet de retrouver les paroles de la chanson courante",
                }
        NotifyModule.__init__(self,
                              bot,
                              desc=desc,
                              pm_allowed=False,
                              name="mpd",
                              delay=0)

        # To limit flood in logs : if the bot can't connect to the server, it will only be notified
        # once in the logfile
        self.error_notified = False
        try:
            self.mpd = BotMPD(self.host, self.port, self.pwd, self.datadir)
            self.mpd_listen = BotMPD(self.host, self.port, self.pwd, self.datadir)
            self.mpd.disconnect()
            self.mpd_listen.disconnect()
        except ConnectionError:
            logger.error("Can't connect to mpd server")
        except NameError:
            self.delay = 60
            logger.error("Error trying to connect to the mpd server")

    @defaultcmd
    def answer(self, sender, message):
        if not message:
            return self.do_command_mpd(self.mpd.current, ())
        else:
            return "N'existe pas ça, RTFM. Ou alors tu sais pas écrire ..."

    def action(self):
        # Here we redefine action (and not do_action as we are supposed to)
        # This is due to the fact that the "async" part here is handled by the idle()
        # function of the mpd library and not by a loop with sleep(delay) as usual
        # Since the delay is fixed to 0, then the 'run' method of NotifyModule becomes
        # def run(self):
        #     while self.alive:
        #         time.sleep(0)
        #         if not self._mute:
        #             self.do_action()
        # If the bot is muted, the action() does not block so there is no block at all !

        try:
            self.mpd_listen.connection(self.host, self.port, self.pwd)
            self.error_notified = False
            self.delay = 0
            self.mpd_listen.send_idle()
            r = self.mpd_listen.fetch_idle()
            repDict = {"The Who - Baba O`riley": "La musique des experts !!!",
                       "The Who - Won't Get Fooled Again": "La musique des experts !!!",
                       "Oledaf et Monsieur D - Le café": "Coffee time !",
                       "Popcorn": "Moi aussi j'aime bien le popcorn",
                       "popcorn": "Moi aussi j'aime bien le popcorn",
                       "Ping Pong": "IPQ charlie est mauvais en ping pong :p",
                       "Daddy DJ": "<xouillet> on écoutait ca comme des dingues à La Souterraine en Creuse \o/ </xouillet>",
                       "Goldman": "JJG !!!",
#                       "Clapton": "<xouillet> owi c'est Joe !!! </xouillet>",
                       "Les 4 barbus - La pince a linge": "LA PINCE A LINGE !!!"}
            repDict["Les 4 barbus - La pince a linge"] = """
|\    /|
| \  / |
|  \/  |
|  ()  |
|_/||  |
|  ()  |
| (  ) |
|  ()  |
|  ||  |
|__/\__| """
            if r is not None and 'player' in r and not self._mute:
                title = self.mpd_listen.currentsongf()
                self.bot.say("Nouvelle chanson : %s" % title)
                for c in repDict:
                    if c in title:
                        self.bot.say(repDict[c])
            self.mpd_listen.disconnect()
        except ConnectionError:
            if not self.error_notified:
                logger.error(_("Can't connect to server %s:%s") % (self.host, self.port))
                self.error_notified = True
                #The module will check again in `self.delay` seconds
                self.delay = 10
        except NameError:
            self.delay = 60
            logger.error("Error trying to connect to the mpd server")

    @answercmd("lyrics")
    def lyrics(self, sender):
        import urllib.request, urllib.parse, urllib.error
        from bs4 import BeautifulSoup
        import re

        self.mpd.connection(self.host, self.port, self.pwd)
        artist = self.mpd.artist()
        title = self.mpd.title()
        self.mpd.disconnect()

        if not artist or not title:
            return "Bad tag"

        ret = artist + " - " + title + "\n"
        url = 'http://lyrics.wikia.com/api.php?action=lyrics&artist=%s&song=%s&fmt=xml&func=getSong' % (artist, title)
        f = urllib.request.urlopen(url)
        soup = BeautifulSoup(f.read())
        f.close()
        if soup.find("lyrics").text != 'Not found':
            url2 = soup.find("url").text
            f2 = urllib.request.urlopen(url2)
            soup = BeautifulSoup(f2.read())
            f2.close()
            text = soup.find("div", {"class": "lyricbox"})
            if text is None:
                ret += "No lyrics available"
            else:
                for tag in text.findAll(True):
                    if tag.name == "div" or tag.name == "p":
                        tag.extract()
                for tag in text.findAll("a"):
                    tag.replaceWith(tag.renderContents())
                for tag in text.findAll("i"):
                    tag.replaceWith(tag.renderContents())
                for tag in text.findAll("b"):
                    tag.replaceWith(tag.renderContents())
                comments = text.findAll(text=lambda text:isinstance(text, BeautifulSoup.Comment))
                [c.extract() for c in comments]
                t = "".join([str(i) for i in text.contents])
                ret2 = str(BeautifulSoup.BeautifulSoup(t, formatter="html")
                ret += re.sub('<br />', '\n', ret2)
        else:
            ret += "No lyrics available"
        return ret.strip()

    @answercmd("current")
    def current(self, sender):
        return self.do_command_mpd(self.mpd.current, ())

    @answercmd("next")
    def next(self, sender):
        return self.do_command_mpd(self.mpd.next_song, [sender])

    @answercmd("prev")
    def prev(self, sender):
        return self.do_command_mpd(self.mpd.prev_song, ())

    @answercmd("list", "list (?P<number>\d+)")
    def list(self, sender, number="5"):
        nb = int(number)
        if nb > 15:
            return "Non mais oh ! Il ne faudrait pas exagérer tout de même."
        return self.do_command_mpd(self.mpd.nextplaylist, [nb])

    @answercmd("settag (artist ?= ?(?P<artist>[^\|]*))? ?\|? ?(title ?= ?(?P<title>.*))?")
    def settag(self, sender, artist, title):
        return self.do_command_mpd(self.mpd.settag, [artist, title])

    @answercmd("shuffle")
    def current(self, sender):
        self.do_command_mpd(self.mpd.shuffle, ())
        return "Et on mélange le tout !"

    @answercmd("setnext (?P<number>\d+)")
    def setnext(self, sender, number):
        nb = int(number)
        return self.do_command_mpd(self.mpd.setnext, [nb])

    @answercmd("nightmare", "nightmare (?P<number>\d+)")
    def nightmare(self, sender, number="5"):
        nb = int(number)
        if nb > 15:
            return "Meriletfou !"
        return self.do_command_mpd(self.mpd.nightmare, [nb])

    @answercmd("coffee", "coffee (?P<number>\d+)")
    def coffee(self, sender, number="5"):
        nb = int(number)
        if nb > 15:
            return "Meriletfou !"
        return self.do_command_mpd(self.mpd.coffee, [nb])

    @answercmd("wakeup", "wakeup (?P<number>\d+)")
    def wakeup(self, sender, number="5"):
        nb = int(number)
        if nb > 15:
            return "Meriletfou !"
        return self.do_command_mpd(self.mpd.wakeup, [nb])

    @answercmd("clean")
    def clean(self, sender):
        return self.do_command_mpd(self.mpd.clean, ())

    @answercmd("goto (?P<position>\d+)")
    def goto(self, sender, position):
        pos = int(position)
        return self.do_command_mpd(self.mpd.goto, [pos])

    @answercmd("search title (?P<title>.*)", "search artist (?P<artist>.*)", "search (?P<search>.*)")
    def search(self, sender, search=None, title=None, artist=None):
        return self.do_command_mpd(self.mpd.search, [search, title, artist])

    def do_command_mpd(self, fct, args):
        self.mpd.connection(self.host, self.port, self.pwd)
        ret = fct(*args)
        self.mpd.disconnect()
        return ret

