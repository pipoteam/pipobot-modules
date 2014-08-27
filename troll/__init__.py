# -*- coding: utf-8 -*-

from datetime import datetime
from os.path import join, dirname
from random import choice
import re

from pipobot.lib.modules import ListenModule
from pipobot.lib.utils import ListConfigParser

DEFAULT_CONFIG = join(dirname(__file__), "answerlist.cfg")


class Troll(ListenModule):
    _config = (("config_path", str, DEFAULT_CONFIG),)

    def __init__(self, bot):
        desc = _(u"Pipo does not like trolls.")
        ListenModule.__init__(self, bot, name='troll', desc=desc)
        self.words = [w.lower() for w in config.get('trolls', 'words')]
        self.friday = config.get('trolls', 'friday')
        self.others = config.get('trolls', 'others')

    def answer(self, sender, message):
        if any(w.lower() in self.words for w in re.findall(r'[a-zA-Z]+', message)):
            if datetime.now().weekday() == 4: # Friday
                return choice(self.friday)
            return choice(self.others)
