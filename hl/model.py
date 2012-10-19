#!/usr/bin/python
# -*- coding: UTF-8 -*-

from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from pipobot.lib.bdd import Base
from pipobot.lib.known_users import KnownUser

association_table = Table('list_members', Base.metadata,
    Column('knownuser_pseudo', String(30), ForeignKey('knownuser.pseudo')),
    Column('hllist_name', String(30), ForeignKey('hllist.name'))
)

class HlList(Base):
    __tablename__ = "hllist"
    name = Column(String(30), primary_key=True)
    members = relationship("KnownUser",
                           secondary=association_table,
                           backref="hllists")

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
