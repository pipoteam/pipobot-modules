# -*- coding: UTF-8 -*-

import requests
from pipobot.lib.bdd import Base
from sqlalchemy import Column, Integer, String


class KickStart(Base):
    __tablename__ = "kickstarter"
    name = Column(String(250), primary_key=True)
    owner = Column(String(250))

    def url(self):
        return 'https://www.kickstarter.com/projects/%s/%s/stats.json' % (self.owner, self.name)

    def status(self):
        ret = "%s: " % self.name
        r = requests.get(self.url())
        if r.status_code == 200:
            json = r.json()['project']
            return ret + _("%s, %s $ pledged") % (json['state'], json['pledged'])
        return ret + _("HTTP status code %i") % r.status_code
