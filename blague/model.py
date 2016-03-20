# -*- coding: UTF-8 -*-
from pipobot.lib.bdd import Base
from sqlalchemy import Column, Integer, String


class Blagueur(Base):
    __tablename__ = "blagues"
    pseudo = Column(String(250), primary_key=True)
    score = Column(Integer)
    submission = Column(Integer)

    def __init__(self, pseudo, score, submission):
        self.pseudo = pseudo
        self.score = score
        self.submission = submission
