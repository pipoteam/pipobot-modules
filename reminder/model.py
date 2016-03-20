# -*- coding: UTF-8 -*-
import time

import pipobot.lib.bdd
from sqlalchemy import Column, Integer, String


class Remind(pipobot.lib.bdd.Base):
    __tablename__ = "remind"
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner = Column(String(250))
    description = Column(String(250))
    date = Column(Integer)
    reporter = Column(String(250))
    room = Column(String(50))

    def __init__(self, owner, description, date, reporter, room):
        self.owner = owner
        self.description = description
        self.date = date
        self.reporter = reporter
        self.room = room

    def __str__(self):
        d = time.strftime("%d/%m/%Y à %H:%M", time.localtime(float(self.date)))
        return u"%s. %s (le %s par %s)" % (self.id, self.description, d.decode("utf-8"), self.reporter)
