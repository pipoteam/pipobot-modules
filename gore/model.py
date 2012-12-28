#!/usr/bin/python
# -*- coding: UTF-8 -*-
from sqlalchemy import Column, Integer, String
from pipobot.lib.bdd import Base


class GoreBase(Base):
    __tablename__ = "gore"
    jid = Column(String(250), primary_key=True)
    score = Column(Integer)
    submission = Column(Integer)

    def __init__(self, jid, score, submission):
        self.jid = jid
        self.score = score
        self.submission = submission

