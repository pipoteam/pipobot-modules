#! /usr/bin/python2
# -*- coding: utf-8 -*-
import time
import re
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, and_, or_
from pipobot.lib.modules import SyncModule, defaultcmd, answercmd
from .model import Dette


class CmdDette(SyncModule):
    """ Gestion de Dettes """
    def __init__(self, bot):
        desc = {"": "Gestionnaire de dettes",
                "add": """dette add [name1] [amount] [name2] [reason] : Ajoute une dette de [amount] que doit payer [name1] à [name2] à cause de [reason]
dette add [name1] [name2] [amount] [name3] [reason] : [name1] et [name2] doivent tous [amount] à [name3] à cause de [reason]""",
                "multiple": "dette multiple [name1] [name2] [amount] [name3] [reason] : [name1] et [name2] doivent se partager la dette [amount] à payer à [name3] à cause de [reason]",
                "list": "dette list [name] : Liste les dettes de [name1]",
                "remove": "dette remove [id1], [id2], [id3] : Supprime les dettes dont les id sont [id1], [id2], [id3]"
                }
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="dette",
                            )

    @defaultcmd
    def answer(self, sender, message):
        return "\n".join("%s: %s" % e for e in self.desc.items())

    @answercmd("list", "list (?P<name1>\S+)(?: )*(?P<name2>\S+)?")
    def list(self, sender, name1=None, name2=None):
        if name1 is None:
            tmp = self.bot.session.query(Dette).order_by(Dette.id).all()
            if tmp == []:
                return "Pas de dettes…"
            else:
                res = "\n " + 21 * "_" + "\n"
                res += "| Toutes les Dettes : |\n"
                res += "|" + 21 * "_" + "|" + 88 * "_" + "\n"
                for elt in tmp:
                    res += "| %s |\n" % elt
                res += "|" + 110 * "_" + "|"
                return {"text": res, "monospace": True}
        else:
            if name2 is None:
                debt_list = self.bot.session.query(Dette, Dette.amount).filter(Dette.debtor == name1).all()
                credit_list = self.bot.session.query(Dette, Dette.amount).filter(Dette.creditor == name1).all()
            else:
                debt_list = self.bot.session.query(Dette, Dette.amount).filter(and_(Dette.debtor == name1, Dette.creditor == name2)).all()
                credit_list = self.bot.session.query(Dette, Dette.amount).filter(and_(Dette.creditor == name1, Dette.debtor == name2)).all()
            n = 0
            p = 0
            res_debt = ""
            res_credit = ""
            if debt_list != []:
                for e in debt_list:
                    n += e[1]
                    res_debt += "| %s|\n" % e[0]
            if credit_list != []:
                for e in credit_list:
                    p += e[1]
                    res_credit += "| %s|\n" % e[0]
            if (n == 0) and (p == 0):
                if name2 is None:
                    return "%s ne doit rien à personne" % (name1)
                else:
                    return "%s ne doit rien à %s" % (name1, name2)
            res = ""

            if name2 is None:
                if p - n > 0:
                    res += "%s doit encore recevoir %s € en tout\n" % (name1, str(p - n))
                else:
                    res += "%s a un déficit de %s € en tout\n" % (name1, str(n - p))
                if n != 0:
                    res += " " + 12 * "_" + "\n"
                    res += "| Dette(s) : |\n"
                    res += "|" + 12 * "_" + "|" + 96 * "_" + "\n"
                    res += res_debt
                    res += "|" + 109 * "_" + "|\n"
                if p != 0:
                    res += " " + 13 * "_" + "\n"
                    res += "| Crédit(s) : |\n"
                    res += "|" + 13 * "_" + "|" + 95 * "_" + "\n"
                    res += res_credit
                    res += "|" + 109 * "_" + "|\n"

            else:
                if p - n > 0:
                    res += "%s doit recevoir %s € de %s\n" % (name1, str(p - n), name2)
                else:
                    res += "%s doit %s € à %s\n" % (name1, str(n - p), name2)
                res += " " + 109 * "_" + "\n"
                res += res_debt
                res += res_credit
                res += "|" + 109 * "_" + "|\n"

            return {"text": res, "monospace": True}

    @answercmd(r"(?P<dtype>add|multiple) (?P<debtor>\S+(?: \S+)*) (?P<amount>(?:\d+)(?:\.\d+)?) (?P<creditor>\S+) (?P<reason>.*)")
    def add(self, sender, dtype, debtor, amount, creditor, reason):
        debtor = debtor.split(' ')
        amount = float(amount)
        if dtype == 'multiple' :
            amount = amount/len(debtor)
        res = ""
        for elt in debtor:
            if elt != creditor:
                dette = Dette(elt, amount, creditor, reason, time.time())
                self.bot.session.add(dette)
                self.bot.session.commit()
                sum_res = func.sum(Dette.amount)
                n = self.bot.session.query(sum_res).filter(and_(Dette.debtor == elt,
                                                                Dette.creditor == creditor)).first()[0]
                p = self.bot.session.query(sum_res).filter(and_(Dette.debtor == creditor,
                                                                Dette.creditor == elt)).first()[0]
                if n is not None and p is not None and (n - p) == 0:
                    deleted = self.bot.session.query(Dette).filter(or_(and_(Dette.debtor == elt, Dette.creditor == creditor), and_(Dette.debtor == creditor, Dette.creditor == elt))).all()
                    for e in deleted:
                        self.bot.session.delete(e)
                    self.bot.session.commit()
                    res += "Les dettes entre %s et %s sont effacées\n" % (elt, creditor)
                else:
                    res += "Ajout de la dette entre %s et %s\n" % (elt, creditor)
            else:
                res += "On ne peut pas avoir une dette avec soi-même...\n"
        return res.rstrip()

    @answercmd("(remove|delete|rm|del) (?P<ids>(\d+,?)+)")
    def remove(self, sender, ids):
        res = []
        for i in ids.split(","):
            n = int(i)
            deleted = self.bot.session.query(Dette).filter(Dette.id == n).first()
            if deleted is None:
                res.append("Pas de dette d'id %s" % (n))
            else:
                self.bot.session.delete(deleted)
                res.append("%s a été supprimé" % (deleted))
        self.bot.session.commit()
        return "\n".join(res)
