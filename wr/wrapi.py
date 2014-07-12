# -*- coding: utf-8 -*-

import json
import urllib.request, urllib.parse, urllib.error

# This key has been generated with the registration form of wordreference
# http://www.wordreference.com/docs/APIregistration.aspx
# It is associated to the 'pipobot' project

API_KEY = "2ed3e"
LANGS = ["ar", "zh", "cz", "en", "fr", "gr", "it", "ja", "ko", "pl", "pt", "ro", "es", "tr"]

class NoTranslation(Exception):
    """ Raised if we can not find a translation """
    pass


class APIAuth(Exception):
    """ Raised if we can not log into the API with our key """
    pass


class InternalError(Exception):
    """ Error during the parsing of the response from wordreference """
    pass


class LangError(Exception):
    """ Raised when you translate in/from a not available language """
    pass


class WordRef(object):
    __slots__ = ('base_url')

    def __init__(self, api_key=API_KEY):
        self.base_url = "http://api.wordreference.com/%s/json" % api_key

    def json_from_url(self, url):
        page = urllib.request.urlopen(url)
        content = page.read()
        page.close()
        if page.getcode() == 404:
            raise APIAuth("Can't log in the wordreference API with this key")

        try:
            ret = json.loads(content.decode("utf-8"))
        except:
            raise InternalError("Error reading wordreference response")

        if "Error" in ret:
            raise NoTranslation(ret["Note"])

        return ret

    def translate(self, frm_lang, out_lang, request):
        if not (frm_lang in LANGS and out_lang in LANGS and (frm_lang == "en" or out_lang == "en")):
            raise LangError("You can translate from or to english only, and with these languages : %s" % ", ".join(LANGS))

        request = urllib.parse.quote(request.encode("utf-8"))
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
        try:
            self._parse(json)
        except:
            raise NoTranslation()

    def _parse(self, json):
        if "PrincipalTranslations" in json["term0"]:
            for id, translation in json["term0"]["PrincipalTranslations"].items():
                self.principal.append(Translation(translation))

        if "original" in json and "Compounds" in json["original"]:
            for id, translation in json["original"]["Compounds"].items():
                self.compounds.append(Translation(translation))

        if "Entries" in json["term0"]:
            for id, translation in json["term0"]["Entries"].items():
                self.principal.append(Translation(translation))

        if "OtherSideEntries" in json["term0"]:
            for id, translation in json["term0"]["OtherSideEntries"].items():
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
        return "%s → %s" % (self.original, ", ".join(str(elt) for elt in self.translations))

    def __repr__(self):
        return str(self)


class Term(object):
    __slots__ = ("term", "pos", "sense", "usage")

    def __init__(self, json):
        self.term = None
        self.pos = None
        self.sense = None
        self.usage = None

        for key, value in json.items():
            setattr(self, key.lower(), value)

    def __str__(self):
        usage = " (%s)" % self.sense if self.sense else ""
        res = "%s%s" % (self.term, usage)
        return res

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    w = WordRef()
    trans = w.translate("ja", "en", "おーい")
    for elt in trans.principal:
        print(elt)
