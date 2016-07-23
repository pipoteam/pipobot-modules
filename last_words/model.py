from pipobot.lib.bdd import Base
from sqlalchemy import Column, ForeignKey, Integer, Text


class LastWords(Base):
    __tablename__ = 'last_words'
    kuid = Column(Integer, ForeignKey('knownuser.kuid'), primary_key=True)
    message = Column(Text(1000))
