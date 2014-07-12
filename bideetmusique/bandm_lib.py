# -*- coding: utf-8 -*-
""" Some functions used to parse content from www.bide-et-musique.com/ """

from datetime import date

from pipobot.lib.utils import xhtml2text, url_to_soup


#CONSTS
HOME_PAGE = "http://www.bide-et-musique.com/programme-webradio.html"
SHOWS = "http://www.bide-et-musique.com/grille.html"
PROG_ID = {"next": 1,
           "prev": 2}
PROGS = HOME_PAGE


def parse_progs(typ=""):
    """ Parsing program page """
    soup = url_to_soup(PROGS)
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
    soup = url_to_soup(SHOWS)
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
    tmp = "%s - %s" % (artist.text.strip(), title.text.strip())
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
    soup = url_to_soup(HOME_PAGE)

    player = soup.find("td", {"id": "player"})
    artist = player.find("p", {"class": "titre-song2"}).text.strip()
    title = player.find("p", {"class": "titre-song"}).text.strip()

    return "%s : %s" % (artist, title)


def lyrics():
    """ Extracts lyrics from the current song in 'bide et musique' """
    soup = url_to_soup(HOME_PAGE)
    souptitle = soup.find("p", {"class": "titre-song"})
    title = souptitle.text
    artist = soup.find("p", {"class": "titre-song2"}).text
    url = "http://www.bide-et-musique.com"
    url = "%s%s" % (url, souptitle.a.get("href"))

    soup = url_to_soup(url)
    tab = soup.find("td", {"class": "paroles"})

    if tab is None:
        return "Pas de paroles disponibles pour %s de %s" % (artist, title)

    tab = tab.contents
    res = "%s - %s\n%s\n" % (artist.strip(), title.strip(), "*" * 30)
    for elt in tab:
        res += xhtml2text(str(elt).strip())
    return res


##########################################################
###  TESTS ###############################################
##########################################################

if __name__ == "__main__":
#    print get_next(5)
#    print get_prev(4)
    print(get_shows(2))
#    print current()
