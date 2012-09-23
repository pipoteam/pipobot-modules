# -*- coding: utf-8 -*-

import BeautifulSoup
import html2text
import feedparser
import hashlib
import time
import sys


def get_content(entry):
    conts = entry.get('content', [])

    if entry.get('summary_detail', {}):
        conts += [entry.summary_detail]

    if conts:
        if "type" in conts:
            if conts.type == "html":
                cleanerhtml = BeautifulSoup.BeautifulSoup(conts.value)
                return html2text.html2text(unicode(cleanerhtml))
            elif conts.type == "text/plain":
                return conts.value

        return conts[0].value

    return ""


def get_id(entry):
    if "id" in entry and entry.id:
        if type(entry.id) is dict:
            return entri.id.values()[0]
        return entry.id

    content = get_content(entry)
    if content and content != "\n":
        if type(content) is unicode:
            content = content.encode("utf-8")
        return hashlib.md5(content).hexdigest()

    if "link" in entry:
        return entry.link


def get_time(entry):
    if "date" in entry:
        date = int(time.mktime(entry.date_parsed))
    elif "published" in entry:
        date = int(time.mktime(entry.published_parsed))
    else:
        date = int(time.time())
    return date

if __name__ == "__main__":
    DEBUG = False
    url = sys.argv[1]
    feeds = feedparser.parse(url)
    for entry in feeds.entries:
        if DEBUG:
            for key, value in entry.iteritems():
                print key, "→", value
                print "*" * 110
        else:
            print "*" * 110
            print get_id(entry)
            print get_time(entry)
            print entry.link
            print entry.title
