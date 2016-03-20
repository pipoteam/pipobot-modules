# -*- coding: UTF-8 -*-
import time

from pipobot.lib.bdd import Base
from sqlalchemy import Column, Float, Integer, String


class Dette(Base):
    __tablename__ = "dette"
    id = Column(Integer, primary_key=True, autoincrement=True)
    debtor = Column(String)
    amount = Column(Float)
    creditor = Column(String)
    reason = Column(String)
    date = Column(Integer)

    def __init__(self, debtor, amount, creditor, reason, date):
        self.debtor = debtor
        self.amount = amount
        self.creditor = creditor
        self.reason = reason
        self.date = date

    def __str__(self):
        t = time.strftime("%d/%m/%Y à %H:%M", time.localtime(float(self.date)))
        t = t.decode("utf-8")
        ret = u"%-2s - %-10s doit %6.2f € à %-10s depuis le %s car : %-30s"
        return ret % (self.id, self.debtor, float(self.amount), self.creditor, t, self.reason)
