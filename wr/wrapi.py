# -*- coding: utf-8 -*-

import simplejson
import urllib

# This key has been generated with the registration form of wordreference
# http://www.wordreference.com/docs/APIregistration.aspx
# It is associated to the 'pipobot' project

API_KEY = "2ed3e"
LANGS = ["ar", "zh", "cz", "en", "fr", "gr", "it", "ja", "ko", "pl", "pt", "ro", "es", "tr"]

class NoTranslation(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class APIAuth(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class InternalError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class LangError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
    

class WordRef(object):
    __slots__ = ('base_url')

    def __init__(self, api_key=API_KEY):
        self.base_url = "http://api.wordreference.com/%s/json" % api_key

    def json_from_url(self, url):
        page = urllib.urlopen(url)
        content = page.read()
        page.close()
        if page.getcode() == 404:
            raise APIAuth("Can't log in the wordreference API with this key")

        try:
            json = simplejson.loads(content)
        except:
            raise InternalError("Error reading wordreference response")

        if "Error" in json:
            raise NoTranslation(json["Note"])

        return json
        
    def translate(self, frm_lang, out_lang, request):
        if not (frm_lang in LANGS and out_lang in LANGS and (frm_lang == "en" or out_lang == "en")):
            raise LangError("You can translate from or to english only, and with these languages : %s" % ", ".join(LANGS))

        request = urllib.quote(request.encode("utf-8"))
        url = "%s/%s%s/%s" % (self.base_url, frm_lang, out_lang, request)
        json = self.json_from_url(url)

        if "Response" in json and json["Response"] == "Redirect":
            json = self.json_from_url("%s%s" % (self.base_url, json["URL"]))

        return Result(json)


class Result(object):
    __slots__ = ("principal", "additional", "compounds")

    def __init__(self, json):
        self.principal = []
        self.additional = []
        self.compounds = []
        self._parse(json)

    def _parse(self, json):
        if "PrincipalTranslations" in json["term0"]:
            for id, translation in json["term0"]["PrincipalTranslations"].iteritems():
                self.principal.append(Translation(translation))

        if "original" in json and "Compounds" in json["original"]:
            for id, translation in json["original"]["Compounds"].iteritems():
                self.compounds.append(Translation(translation))

        if "Entries" in json["term0"]:
            for id, translation in json["term0"]["Entries"].iteritems():
                self.principal.append(Translation(translation))

        if "OtherSideEntries" in json["term0"]:
            for id, translation in json["term0"]["OtherSideEntries"].iteritems():
                self.principal.append(Translation(translation))
            

class Translation(object):
    __slots__ = ("original", "translations")
    secondary_translations = ["FirstTranslation", "SecondTranslation", "ThirdTranslation"]

    def __init__(self, json):
        self.original = None
        self.translations = []

        if "OriginalTerm" in json:
            self.original = Term(json["OriginalTerm"])

        for secondary in self.secondary_translations:
            if secondary in json:
                t = Term(json[secondary])
                self.translations.append(t)

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return u"%s → %s" % (self.original, ", ".join(unicode(elt) for elt in self.translations))
        

    def __repr__(self):
        return str(self)


class Term(object):
    __slots__ = ("term", "pos", "sense", "usage")

    def __init__(self, json):
        for attr in self.__slots__:
            setattr(self, attr, None)

        for key, value in json.iteritems():
            setattr(self, key.lower(), value)

    def __unicode__(self):
        usage = u" (%s)" % self.sense if self.sense else ""
        res = u"%s%s" % (self.term, usage)
        return res

    def __str__(self):
        rep = unicode(self).encode("utf-8")
        return rep

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    w = WordRef()
    trans = w.translate("ja", "en", u"おーい")
    for elt in trans.principal:
        print elt
