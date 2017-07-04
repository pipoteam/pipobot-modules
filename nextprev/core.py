# -*- coding: UTF-8 -*-
import pytvmaze
from time import strptime, strftime

alias = {'himym': 'how i met your mother',
         'got': 'game of thrones',
         'tbbt': 'the big bang theory'}
baseurl = "http://services.tvrage.com/tools/quickinfo.php?show=%s"


def convert_episode(ep):
    airdate = strptime(ep.airdate, "%Y-%m-%d")
    airdate = strftime("%d/%m/%Y", airdate)
    return "%sx%s: %s le %s" % (ep.season_number, ep.episode_number, ep.title, airdate)


def getdata(message, isnext):
    if message == "":
        return "Avec un nom de série ça serait mieux !!"

    maze = pytvmaze.TVMaze()

    message = alias.get(message, message)

    try:
        show = maze.get_show(show_name=message)
    except pytvmaze.exceptions.ShowNotFound:
        return "Je n'ai aucune information sur la série %s" % message


    if isnext:
        next_ep = show.next_episode

        if show.status == "Ended":
            return "Désolé mais la série %s est terminée." % show.name

        if not next_ep:
            return "Aucune date pour un prochain épisode :s."

        return "Prochain épisode de %s: %s." % (show.name, convert_episode(next_ep))
    else:
        prev_ep = show.previous_episode
        if not prev_ep:
            return "Aucune info disponible."

        return "Précédent épisode de %s: %s." % (show.name, convert_episode(prev_ep))
