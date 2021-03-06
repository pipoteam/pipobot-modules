# -*- coding: utf-8 -*-

import csv
import datetime
import os
import time
import urllib

from pipobot.lib.module_test import ModuleTest
from pipobot.lib.modules import SyncModule, defaultcmd

ROOT_URL = 'http://www.banque-france.fr/fileadmin/user_upload/banque_de_france/' \
           'Economie_et_Statistiques/Changes_et_Taux/'
CACHE_PATH = "/tmp"
VALUES = {'CHF': 'qs.d.ceurchci.csv', 'USD': 'qs.d.ceurusci.csv',
          'JPY': 'qs.d.ceurjpci.csv', 'CAD': 'qs.d.ceurcaci.csv'}
CACHE_LIMIT = 2 * 3600


class CmdBourse(SyncModule):
    def __init__(self, bot):
        desc = u"""bourse [valeur [historique]]
Affiche le taux de conversion d'une valeur boursière.
Valeurs disponibles: %s""" % (', '.join(VALUES.keys()))
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="bourse")

    @defaultcmd
    def answer(self, sender, message):
        try:
            valeur = message.split(' ')[0]
            histo = int(message.split(' ')[1])
        except:
            valeur = message
            histo = 3

        if not(valeur in VALUES.keys()):
            return self.desc

        # if the file is too old or does not exist, retrive it again
        cache_file = os.path.join(CACHE_PATH, VALUES[valeur])
        if not os.path.isfile(cache_file) or os.path.getmtime(cache_file) + CACHE_LIMIT <= time.time():
            distant_file = u"%s%s" % (ROOT_URL, VALUES[valeur])
            urllib.urlretrieve(distant_file, cache_file)

        # Opening file
        f = open(cache_file, "rb")
        reader = csv.reader(f, delimiter=';')

        # Useless headers to skip
        useless_header = 8

        # Reading actual data
        data = []
        line_no = 0
        for line in reader:
            if line_no < useless_header:
                line_no += 1
            else:
                data.append((line[0], line[1]))

        # Extracting last (histo) values
        output = [u"Dernières valeurs: "]
        output += [u"%s : %s %s / 1€" % (date, value, valeur) for date, value in data[-histo::]]

        return "\n".join(output)


class BourseTest(ModuleTest):
    def test_ok(self):
        today = datetime.date.today()
        regexp = u"Dernières valeurs: "
        for i in range(3, 0, -1):
            day = today + datetime.timedelta(days=-i)
            regexp += u"\n%s : (\d+)(,\d+)? %s / 1€" % (day.strftime("%d/%m/%Y"), "%(currency)s")

        for currency in VALUES:
            bot_rep = self.bot_answer("!bourse %s" % currency)
            self.assertRegexpMatches(bot_rep, regexp % {"currency": currency})

    def test_fail(self):
        bot_rep = self.bot_answer("!bourse PIPO")
        desc = u"""bourse [valeur [historique]]
Affiche le taux de conversion d'une valeur boursière.
Valeurs disponibles: %s""" % (', '.join(VALUES.keys()))
        self.assertEqual(bot_rep, desc)
