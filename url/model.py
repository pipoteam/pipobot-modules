# -*- coding: UTF-8 -*-
import datetime

from pipobot.lib.bdd import Base
from sqlalchemy import Column, DateTime, Integer, String


class RepostUrl(Base):
    __tablename__ = "url"
    url = Column(String(250), primary_key=True)
    count = Column(Integer)
    title = Column(String(250))
    date = Column(DateTime)
    last_date = Column(DateTime)
    jid = Column(String(250))
    chan = Column(String(250))

    def __init__(self, url, jid, chan, title=""):
        self.url = url
        self.jid = jid
        self.count = 1
        self.title = title
        self.date = datetime.datetime.now()
        self.last_date = self.date
        self.chan = chan
