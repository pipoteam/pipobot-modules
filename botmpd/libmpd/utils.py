#!/usr/bin/python
# -*- coding: UTF-8 -*-


def humanize_time(secs):
    secs = int(secs.partition(".")[0])
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    secs = str(secs).zfill(2)
    mins = str(mins).zfill(2)
    hours = str(hours).zfill(2)
    return '%sh%sm%ss' % (hours, mins, secs)


def format(song):
    """Formatte joliment un fichier"""
    artist = song.get("artist", "<unknown>")
    title = song.get("title", "<unknown>")

    if artist == "<unknown>" and title == "<unknown>":
        return "%s. %s" % (song["pos"], song["file"])
    else:
        return "%s. %s - %s" % (song["pos"], artist, title)
