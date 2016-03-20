# -*- coding: UTF-8 -*-
from pipobot.lib.bdd import Base
from sqlalchemy import Column, Integer, String


class HiddenBase(Base):
    __tablename__ = "hidden"
    jid = Column(String(250), primary_key=True)
    score = Column(Integer)

    def __init__(self, jid, score):
        self.jid = jid
        self.score = score
