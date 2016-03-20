# -*- coding: UTF-8 -*-

from pipobot.lib.bdd import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship


class KnownUserTimeZone(Base):
    __tablename__ = "memberstimezones"
    kuid = Column(Integer, ForeignKey('knownuser.kuid'), primary_key=True)
    timezone = Column(String(40))
    user = relationship('KnownUser', backref=backref("user", uselist=False))
