# -*- coding: UTF-8 -*-
import datetime
import re
import urllib

alias = {'himym': 'how i met your mother',
         'got': 'game of thrones'}
baseurl = "http://services.tvrage.com/tools/quickinfo.php?show=%s"


def convert_episode(raw):
    match = re.match("(?P<season>\d+)x(?P<episode>\d+)\^(?P<title>[^\^]*)\^(?P<date>.*)", raw)
    res = match.groupdict()
    try:
        res["date"] = datetime.datetime.strptime(res["date"], "%b/%d/%Y")
        res["date"] = res["date"].strftime("%d/%m/%y")
    except ValueError:
        # If we can't convert the date, we keep it as it was
        pass
    return "%(season)sx%(episode)s: %(title)s le %(date)s" % res


def getdata(message, isnext):
    message = alias.get(message, message)

    show_url = baseurl % (message.replace(" ", "%20"))
    response = urllib.urlopen(show_url)
    content = response.readlines()
    response.close()
    data = {}

    if content == ['No Show Results Were Found For "%s"' % message]:
        return u"Je n'ai aucune information sur la série %s" % message

    for line in content:
        key, value = line.split("@", 1)
        data[key] = value.strip()

    if isnext:
        if data["Status"] == "Canceled/Ended":
            return u"Désolé mais la série %s est terminée." % (data["Show Name"])

        if "Next Episode" in data:
            data_episode = convert_episode(data["Next Episode"])
            return u"Prochain épisode de %s: %s." % (data["Show Name"], data_episode)
        else:
            return u"Aucune date pour un prochain épisode :s."
    else:
        if "Latest Episode" in data:
            data_episode = convert_episode(data["Latest Episode"])
            return u"Précédent épisode de %s: %s." % (data["Show Name"], data_episode)
        else:
            return u"Aucune info disponible."
