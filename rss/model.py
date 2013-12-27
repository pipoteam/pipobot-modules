# -*- coding: utf-8 -*-
import time
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .metadata import Base


class Feed(Base):
    __tablename__ = "feed"
    url = Column(String(250), primary_key=True)
    name = Column(String(250))
    active = Column(Boolean)
    entries = relationship("Entry", backref="feed_owner")
    twitter = Column(Boolean)

    def __init__(self, url, name, twitter=False):
        self.url = url
        self.name = name
        self.twitter = twitter
        self.active = True

    def __str__(self):
        if self.twitter:
            return "%s : Flux twitter https://twitter.com/%s" % (self.name, self.name)
        else:
            return "%s : %s" % (self.name, self.url)


class Entry(Base):
    __tablename__ = "entry"
    rssid = Column(String(250), primary_key=True)
    url = Column(String(250))
    title = Column(String(250))
    date = Column(Integer)
    new = Column(Boolean)
    feed_url = Column(String, ForeignKey("feed.url"))
    feed = relationship(Feed, primaryjoin=feed_url == Feed.url)

    def __init__(self, rssid, url, date, title):
        self.rssid = rssid
        self.url = url
        self.title = title
        self.date = date
        self.new = True
