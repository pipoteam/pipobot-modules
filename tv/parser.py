# -*- coding: utf-8 -*-
from pipobot.lib.utils import xhtml2text, url_to_soup


url = "http://www.programme-tv.net/programme/programme-tnt.html"


def extract():
    soup = url_to_soup(url)
    programs = {}

    for channel in soup.findAll("div", {"class": "channel"}):
        channel_name = channel.find("span").get("title")
        channel_name = channel_name.split("Programme de ")[1]

        channel_data = []
        for prog in channel.findAll("div", {"class": "programme"}):
            heure = prog.find("span", {"class": "prog_heure"}).text
            try:
                nom = prog.find("a", {"class": "prog_name"}).text
            except AttributeError:
                nom = prog.find("span", {"class": "prog_name"}).text
            channel_data.append("%s - %s" % (heure, nom))
        channel_data = " / ".join(channel_data)
        programs[channel_name.lower()] = xhtml2text(channel_data)

    return programs

if __name__ == "__main__":
    e = extract()
