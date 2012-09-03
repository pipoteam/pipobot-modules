#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pipobot.lib.bdd import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class HlList(Base):
    __tablename__ = "hllist"
    hlid = Column(Integer, primary_key=True)
    name = Column(String(30))
    members = relationship("HlListMembers")

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class HlListMembers(Base):
    __tablename__ = "hllistmembers"
    hllist_hlid = Column(Integer, ForeignKey('hllist.hlid'), primary_key=True)
    knownuser_kuid = Column(Integer, ForeignKey('knownuser.kuid'), primary_key=True)
    user = relationship('KnownUser')

    def __init__(self, hlid, kuid):
        self.hllist_hlid = hlid
        self.knownuser_kuid = kuid
