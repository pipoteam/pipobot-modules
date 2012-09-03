#!/usr/bin/python
# -*- coding: UTF-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pipobot.lib.bdd import Base


class CmdAlacons(Base):
    __tablename__ = "cmdalacons"
    cmid = Column(Integer, primary_key=True)
    cmd = Column(String(50))
    desc = Column(String(250))
    answers = relationship("answersalacon")

    def __init__(self, cmd, desc):
        self.cmd = cmd
        self.desc = desc


class AnswersAlacon(Base):
    __tablename__ = "answersalacon"
    ansid = Column(Integer, primary_key=True)
    cmid = Column(Integer, ForeignKey('cmdalacons.cmid'))
    answer = Column(String(250))
    ansto = Column(Integer) # 1: Sender, 2: Nobody, 3: Bot, 4: Somebody, 5: Something

    def __init__(self, cmid, answer, ansto):
        self.cmid = cmid
        self.answer = answer
        self.ansto = ansto
