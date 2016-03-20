# -*- coding: UTF-8 -*-
import config
import urllib
from xml.dom import minidom


class UnknownEmission(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Emission inconnue : %s" % self.name


class QualityException(Exception):
    def __init__(self, quality, vid):
        self.quality = quality
        self.vid = vid

    def __str__(self):
        return "Qualité inconnue pour la vidéo %s : %s " % (self.vid, self.msg)


class Video:
    def __init__(self, id, title, subtitle):
        self._id = id
        self.title = title
        self.subtitle = subtitle
        self.url = "%s/%s" % (config.urlXMLVid, self._id)
        self.links = {}
        self.update()

    def __str__(self):
        return "%s - %s" % (self.title, self.subtitle)

    def get_id(self):
        return self._id

    def set_id(self, new_id):
        self._id = new_id
        self.url = "%s/%s" % (config.urlXMLVid, self._id)

    id = property(get_id, set_id)

    def update(self):
        page = urllib.urlopen(self.url)
        self.url = "%s/%s" % (config.urlXMLVid, self.id)
        content_page = page.read()
        page.close()
        video_xml = minidom.parseString(content_page)
        for quality in config.qualities:
            video = video_xml.getElementsByTagName("MEDIA")[0].getElementsByTagName("VIDEOS")[0]
            try:
                self.links[quality] = video.getElementsByTagName(quality)[0].childNodes[0].nodeValue
            except KeyError:
                # This quality does not exist for this show
                pass

    def get_url(self, quality):
        try:
            return self.links[quality]
        except KeyError:
            raise QualityException(self.title, quality)


class Emission:
    def __init__(self, name, notif=False):
        try:
            self.id = config.emissions_id[name]
            self.name = name
            self.url = "%s/%s" % (config.urlXMLEmissions, self.id)
            id, title, subtitle = self.update_data()
            self.last_vid = Video(id, title, subtitle)
            self.notif = notif
        except KeyError:
            raise UnknownEmission(name)

    def update_data(self):
        page = urllib.urlopen(self.url)
        content_page = page.read()
        page.close()

        data = minidom.parseString(content_page)
        mea = data.getElementsByTagName("MEA")[0]
        id = mea.getElementsByTagName("ID")[0].childNodes[0].nodeValue
        title = mea.getElementsByTagName("TITRE")[0].childNodes[0].nodeValue
        try:
            subtitle = mea.getElementsByTagName("SOUS_TITRE")[0].childNodes[0].nodeValue
        except IndexError:
            subtitle = ""
        return id, title, subtitle

    def update(self):
        id, title, subtitle = self.update_data()
        if id > self.last_vid.id:
            self.last_vid.id = id
            self.last_vid.title = title
            self.last_vid.subtitle = subtitle
            self.last_vid.update()
            return True
        return False
