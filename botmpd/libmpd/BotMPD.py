# -*- coding: utf-8 -*-
import os
import random
from mpd import MPDClient, ConnectionError, CommandError
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import utils
import threading


class BotMPD(MPDClient):
    def __init__(self, host, port, password, datadir=None):
        self.token = threading.Lock()
        MPDClient.__init__(self)
        if not self.connection(host, port, password):
            self.disconnect()
            raise NameError("Mauvais hôte ou mot de passe MPD")
        if not datadir:
            self.datadir = None
        else:
            self.datadir = datadir

    def currentsongf(self):
        song = self.currentsong()
        return utils.format(song)

    def current(self):
        song = self.currentsong()
        playlist = self.status()

        res = self.currentsongf() + "\n"
        res += "[playing] #%s/%s" % (song["pos"], playlist["playlistlength"])
        if 'time' in list(playlist.keys()):
            current, total = playlist['time'].split(':')
            pcentage = int(100 * float(current) / float(total))
            res += "  %s/%s (%s%%)" % (utils.humanize_time(current),
                                       utils.humanize_time(total),
                                       pcentage)
        return res

    def nextplaylist(self, nb):
        current = self.currentsong()
        playlist = self.playlistinfo()
        deb = int(current['pos'])
        end = int(self.status()["playlistlength"])
        res = ""
        for i in range(nb):
            song = playlist[(deb + i) % end]
            res += utils.format(song) + "\n"
        return res[:-1]

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
        res = ""
        for elt in req:
            res += "%s\n" % (utils.format(elt))
        return res[0:-1]

    def setnext(self, nb):
        song = self.currentsong()
        current = song["pos"]
        icurrent = int(current)
        if nb < icurrent:
            newindex = icurrent
        else:
            newindex = icurrent + 1
        try:
            self.move(nb, newindex)
            return self.nextplaylist(3)
        except CommandError:
            return "Bad song index"

    def nightmare(self, nb):
        self.update()
        try:
            songs = self.lsinfo("nightmare")
        except CommandError:
            return "No directory named nightmare"
        self.add_mpd(songs, nb)
        return "/!\\/!\\/!\\/!\\"

    def coffee(self, nb):
        self.update()
        try:
            songs = self.lsinfo("coffee")
        except CommandError:
            return "No directory named coffee"
        self.add_mpd(songs, nb)
        return "Coffee en préparation"

    def wakeup(self, nb):
        self.update()
        try:
            songs = self.lsinfo("wakeup")
        except CommandError:
            return "No directory named wakeup"
        self.add_mpd(songs, nb)
        return "ON SE REVEILLE !!!"

    def add_mpd(self, l, nb):
        random.shuffle(l)
        if nb < len(l):
            selection = l[0:nb]
        else:
            selection = l
        playlist = self.status()
        deb = int(playlist["playlistlength"])
        for elt in selection:
            self.add(elt["file"])
        for i in range(deb, deb + nb):
            self.setnext(i)

    def goto(self, pos):
        try:
            song = self.currentsong()
            current = song["pos"]
            icurrent = int(current)
            self.move(icurrent, pos)
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
        mess = []
        song = self.currentsong()["file"]
        f = os.path.join(self.datadir, song)
        try:
            mp3 = MP3(f, ID3=EasyID3)
        except IOError as e:
            if e.errno == 13:
                return "Je n'ai pas le droit de lire ce fichier :'("
        try:
            mp3['artist'] = artist
            mp3['title'] = title
            mp3.save()
            self.update()
            mess.append("Règle artist en %s" % (artist))
            mess.append("Règle title en %s" % (title))
        except IOError:
            return "Je n'ai pas le droit d'éditer ce fichier :'("
        return "\n".join(mess)

    def artist(self):
        try:
            return self.currentsong()['artist']
        except KeyError:
            return None

    def title(self):
        try:
            return self.currentsong()['title']
        except KeyError:
            return None

    def next_song(self, sender):
        ret = "%s ne veut pas écouter : %s" % (sender, self.currentsongf())
        next(self)
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
       except ConnectionError as e:
           return False

    def disconnect(self):
        MPDClient.disconnect(self)
        self.token.release()
