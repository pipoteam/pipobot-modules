#!/usr/bin/python
# -*- coding: UTF-8 -*-

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from pipobot.lib.bdd import Base


class KnownUserTimeZone(Base):
    __tablename__ = "memberstimezones"
    kuid = Column(Integer, ForeignKey('knownuser.kuid'), primary_key=True)
    timezone = Column(String)
    user = relationship('KnownUser')
