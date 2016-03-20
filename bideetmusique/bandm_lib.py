# -*- coding: utf-8 -*-
""" Some functions used to parse content from www.bide-et-musique.com/ """
import urllib
from datetime import date

from BeautifulSoup import BeautifulSoup
from pipobot.lib.utils import xhtml2text


class AppURLopener(urllib.FancyURLopener):
    """ Redefines the AppURLopener that could contain a wrong
        User-Agent """
    pass

# CONSTS

PLAYLIST = 'http://www.bide-et-musique.com/playlist.rss'
PROGS = "http://www.bide-et-musique.com/programme-webradio.html"
SHOWS = "http://www.bide-et-musique.com/grille.html"
PROG_ID = {"next": 1,
           "prev": 2}
HOME_PAGE = "http://www.bide-et-musique.com/programme-webradio.html"


def parse_progs(typ=""):
    """ Parsing program page """
    page = urllib.urlopen(PROGS)
    content = page.read()
    page.close()
    soup = BeautifulSoup(content)
    tables = soup.findAll("table", {"class": "bmtable"})
    soup = tables[PROG_ID[typ]]
    return soup

####################################################
###   PARSING show list ############################
####################################################


def parse_one_show(soup_show):
    """ Extracts data from a program in bide et musique """
    tds = soup_show.findAll("td")
    hour = xhtml2text(tds[0].text)
    name = xhtml2text(tds[1].text)
    return "%s - %s" % (hour, name)


def get_shows(day=None):
    """ Extracts the list of all shows from a given day """
    nb_day = date.today().weekday()
    if day is not None:
        nb_day = ((nb_day + day) % 7) + 1
    page = urllib.urlopen(SHOWS)
    content = page.read()
    page.close()
    soup = BeautifulSoup(content)
    table = soup.find("table", {"class": "bmtable"})
    res = []
    found = False
    for tr in table.findAll("tr"):
        id_tag = tr.get("id")
        if id_tag is None:
            if found:
                res.append(parse_one_show(tr))
        else:
            _, id = id_tag.split("_", 1)
            if int(id) == nb_day:
                found = True
            elif found:
                break
    return "\n".join(res)

####################################################
###   PARSING track list ###########################
####################################################


def get_prev(nb=1):
    """ Returns last song played in b&m """
    progs = parse_progs("prev")
    return parse_tracks(progs, nb)


def get_next(nb=1):
    """ Returns next song int the b&m playlist """
    progs = parse_progs("next")
    return parse_tracks(progs, nb)


def parse_one_track(soup_track):
    """ Extracts infos of a track from HTML code of b&m pages """
    artist, title = soup_track.findAll("td", {"class": "baseitem"})
    tmp = "%s - %s" % (artist.text, title.text)
    return xhtml2text(tmp)


def parse_tracks(soup, nb=1):
    """ Extracts track list from HTML of b&m """
    tracks = soup.findAll("tr")
    res = []
    for track in tracks:
        try:
            res.append(parse_one_track(track))
        except ValueError:
            pass
    return "\n".join(res[0:nb])


def current():
    """ Returns current track """
    page = urllib.urlopen(PLAYLIST)
    content = page.read(1500)
    page.close()
    soup = BeautifulSoup(content)
    try:
        return xhtml2text(xhtml2text(soup.findAll("title")[1].text.partition(": ")[2]))
    except:
        return "HTML parsing failed !"


def lyrics():
    """ Extracts lyrics from the current sont in 'bide et musique' """
    res = ""
    page = urllib.urlopen(HOME_PAGE)
    content = page.read()
    page.close()
    soup = BeautifulSoup(content)
    souptitle = soup.findAll("p", {"class": "titre-song"})[0]
    title = souptitle.text
    artist = soup.findAll("p", {"class": "titre-song2"})[0].text
    souptitle = soup.findAll("p", {"class": "titre-song"})[0]
    url = "http://www.bide-et-musique.com"
    url = "%s%s" % (url, souptitle.a.get("href"))
    page = urllib.urlopen(url)
    content = page.read()
    page.close()
    soup = BeautifulSoup(content)
    tab = soup.findAll("td", {"class": "paroles"})
    if tab == []:
        res = "Pas de paroles disponibles pour %s de %s" % (artist, title)
    else:
        tab = tab[0].contents
        res = "%s - %s\n%s\n" % (artist, title, "*" * 30)
        lyrics_content = ""
        for elt in tab:
            tmp = elt
            if str(tmp).lstrip() != "<br />":
                lyrics_content += xhtml2text(unicode(tmp).lstrip()) + "\n"
        res += lyrics_content
    return xhtml2text(res)


##########################################################
###  TESTS ###############################################
##########################################################

if __name__ == "__main__":
    # print get_next(5)
    # print get_prev(4)
    print get_shows(2)
    # print current()
