#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import operator
from pipobot.lib.modules import SyncModule
from pipobot.lib.known_users import KnownUser
from abstractblague import AbstractBlague
from model import Blagueur


class CmdBlague(AbstractBlague):
    """ Ajoute un point-blague à un collègue blagueur compétent """
    def __init__(self, bot):
        desc = (u"Donnez un point blague à un ami ! Écrivez !blague pseudo "
                u"(10 s minimum d'intervalle)")
        AbstractBlague.__init__(self,
                                bot,
                                desc=desc,
                                name="blague",
                                autocongratulation="Un peu de modestie, merde",
                                premier=u"Félicitations %s, c'est ta première blague !",
                                operation=operator.add)

    def cmd_score(self, sender, message):
        """Affiche les scores des blagueurs"""
        classement = self.bot.session.query(Blagueur).all()
        if len(classement) != 0:
            classement.reverse()
            sc = "\nBlagounettes - scores :"
            pseudo = ""
            sc += "\n" + 75 * "_"
            classement = self.regroup_scores(classement)
            for pseudo, score in classement:
                sc += "\n| %-4s  -  " % (score[0])
                if len(pseudo) > 30:
                    sc += "%s " % (pseudo[:30])
                else:
                    sc += "%-30s " % (pseudo)
                sc += time.strftime(" dernière le %d/%m/%Y à %H:%M |",
                                    time.localtime(score[1]))
            sc += "\n|" + 73 * "_" + "|"
            return {"text": sc, "monospace": True}
        else:
            return "Aucune blague, bande de nuls !"

    def regroup_scores(self, classement):
        result = {}
        for blag in classement:
            known = KnownUser.get(blag.pseudo, self.bot)
            #if the jid in the database is a known user
            if known:
                # if we already have an entry for him with a different jid
                if known.pseudo in result:
                    result[known.pseudo] = (result[known.pseudo][0] + blag.score,
                                            max(blag.submission, result[known.pseudo][1]))
                else:
                    #else we create it
                    result[known.pseudo] = (blag.score, blag.submission)
            else:
                #We do not know him : we use his jid
                result[blag.pseudo] = (blag.score, blag.submission)
        result = sorted(result.iteritems(),
                        key=operator.itemgetter(1), reverse=True)
        return result
