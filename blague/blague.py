#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import operator
from pipobot.lib.known_users import KnownUser
from .abstractblague import AbstractBlague
from .model import Blagueur

tab_header = """
Blagounettes - scores:
__________________________________________________________________________"""

tab_line = """
| %(score)-4s  -  %(jid)-30s dernière %(date)s | """

tab_footer = """
|________________________________________________________________________|"""


class CmdBlague(AbstractBlague):
    """ Ajoute un point-blague à un collègue blagueur compétent """

    def __init__(self, bot):
        desc = ("Donnez un point blague à un ami ! Écrivez !blague pseudo "
                "(10 s minimum d'intervalle)")
        AbstractBlague.__init__(self,
                                bot,
                                desc=desc,
                                name="blague",
                                autocongratulation="Un peu de modestie, merde",
                                premier="Félicitations %s, c'est ta première blague !",
                                operation=operator.add)

    def cmd_score(self, sender, message):
        """Affiche les scores des blagueurs"""

        classement = self.get_scores()
        if classement == []:
            return "Aucune blague, bande de nuls !"

        sc = tab_header

        for pseudo, (score, last_blague) in classement:
            date = time.strftime("le %d/%m/%Y à %H:%M",
                                 time.localtime(last_blague))
            sc += tab_line % {"score": score,
                              "jid": pseudo[:30],
                              "date": date
                             }
        sc += tab_footer
        return {"text": sc, "monospace": True}

    def get_scores(self):
        classement = self.bot.session.query(Blagueur).all()
        result = {}
        for blag in classement:
            known = KnownUser.get(blag.pseudo, self.bot)
            #if the jid in the database is a known user
            if known:
                # if we already have an entry for him with a different jid
                if known.get_pseudo() in result:
                    old_score, old_time = result[known.get_pseudo()]
                    result[known.pseudo] = (old_score + blag.score,
                                            max(blag.submission, old_time))
                else:
                    #else we create it
                    result[known.get_pseudo()] = (blag.score, blag.submission)
            else:
                #We do not know him : we use his jid
                result[blag.pseudo] = (blag.score, blag.submission)
        result = sorted(iter(result.items()),
                        key=operator.itemgetter(1), reverse=True)
        return result
