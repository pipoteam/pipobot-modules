# -*- coding: utf-8 -*-
import os
import random
from mpd import MPDClient, ConnectionError, CommandError
from mutagenx.easyid3 import EasyID3
from mutagenx.mp3 import MP3
from . import utils
import threading


class BotMPD(MPDClient):
    def __init__(self, host, port, password, datadir=None):
        self.token = threading.Lock()
        MPDClient.__init__(self)

        if not self.connection(host, port, password):
            self.disconnect()
            raise NameError("Mauvais hôte ou mot de passe MPD")

        self.datadir = datadir

    def _current_pos(self):
        current = self.currentsong()
        return int(current['pos'])

    def currentsongf(self):
        song = self.currentsong()
        return utils.format(song)

    def current(self):
        song = self.currentsong()
        playlist = self.status()

        res = "%s\n" % utils.format(song)
        res += "[playing] #%s/%s" % (song["pos"], playlist["playlistlength"])

        if 'time' in playlist:
            current, total = playlist['time'].split(':')
            pcentage = int(100 * float(current) / float(total))
            res += "  %s/%s (%s%%)" % (utils.humanize_time(current),
                                       utils.humanize_time(total),
                                       pcentage)
        return res

    def nextplaylist(self, nb):
        playlist = self.playlistinfo()
        deb = self._current_pos()
        end = int(self.status()["playlistlength"])
        res = ""
        for i in range(nb):
            song = playlist[(deb + i) % end]
            res += utils.format(song) + "\n"
        return res.strip()

    def search(self, search, title, artist):
        req = []
        if search:
            req = self.playlistsearch("Artist", search)
            req.extend(self.playlistsearch("Title", search))
        elif title:
            req = self.playlistsearch("Title", title)
        elif artist:
            req = self.playlistsearch("Artist", artist)

        if req == []:
            return "Cherches un peu mieux que ça"

        res = "\n".join(map(utils.format, req))
        return res

    def setnext(self, nb):
        icurrent = self._current_pos()

        if nb < icurrent:
            newindex = icurrent
        else:
            newindex = icurrent + 1

        try:
            self.move(nb, newindex)
            return self.nextplaylist(3)
        except CommandError:
            return "Bad song index"

    def add_from_dir(self, dir, nb, msg):
        self.update()
        try:
            songs = self.lsinfo(dir)
        except CommandError:
            return "No directory named %s" % dir

        random.shuffle(songs)
        selection = songs[0:nb]

        playlist = self.status()
        deb = int(playlist["playlistlength"])
        for elt in selection:
            self.add(elt["file"])
        for i in range(deb, deb + nb):
            self.setnext(i)
        return msg

    def nightmare(self, nb):
        return self.add_from_dir("nightmare", nb, "/!\\/!\\/!\\/!\\")

    def coffee(self, nb):
        return self.add_from_dir("coffee", nb, "Coffee en préparation")

    def wakeup(self, nb):
        return self.add_from_dir("wakeup", nb, "ON SE REVEILLE")

    def goto(self, pos):
        try:
            current = self._current_pos()
            self.move(current, pos)
            return "On s'est déplacé en %s !" % pos
        except CommandError:
            return "Et un goto foiré, un !"

    def clean(self):
        nightmare = self.lsinfo("nightmare")
        playlist = self.playlistinfo()
        for elt in nightmare:
            for eltplaylist in playlist:
                if elt["file"] == eltplaylist["file"]:
                    self.deleteid(eltplaylist["id"])
        return "Sauvé...mais pour combien de temps..."

    def settag(self, artist, title):
        if self.datadir is None:
            return "Impossible, datadir non spécifié"

        song = self.currentsong()["file"]
        f = os.path.join(self.datadir, song)

        try:
            mp3 = MP3(f, ID3=EasyID3)
        except IOError as e:
            return "Je n'ai pas le droit de lire ce fichier :'("

        try:
            mp3['artist'] = artist
            mp3['title'] = title
            mp3.save()
            self.update()
            mess = "Règle artist en %s\n" % (artist)
            mess += "Règle title en %s" % (title)
        except IOError:
            return "Je n'ai pas le droit de modifier ce fichier :'("

        return mess

    def artist(self):
        return self.currentsong().get('artist')

    def title(self):
        return self.currentsong().get('title')

    def next_song(self, sender):
        ret = "%s ne veut pas écouter : %s" % (sender, self.currentsongf())
        self.next()
        return ret

    def prev_song(self):
        self.previous()
        return "On revient à %s" % (self.currentsongf())

    def connection(self, host, port, pwd):
        self.token.acquire()
        try:
            self.connect(host, port)
            self.password(pwd)
            return True
        except ConnectionError:
            return False

    def disconnect(self):
        MPDClient.disconnect(self)
        self.token.release()
