# -*- coding: utf-8 -*-
import time
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from metadata import Base


class Feed(Base):
    __tablename__ = "feed"
    url = Column(String(250), primary_key=True)
    name = Column(String(250))
    active = Column(Boolean)
    entries = relationship("Entry", backref="feed_owner")

    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.active = True

    def __str__(self):
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
