#! /usr/bin/python2
# -*- coding: utf-8 -*-
import time
import re
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, and_, or_
from pipobot.lib.modules import SyncModule, defaultcmd, answercmd
from model import Dette

class CmdDette(SyncModule):
    """ Gestion de Dettes """
    def __init__(self, bot):
        desc = {"" : u"Gestionnaire de dettes",
                "add" : u"""dette add [name1] [amount] [name2] [reason] : Ajoute une dette de [amount] que doit payer [name1] à [name2] à cause de [reason]
dette add [name1] [name2] [amount] [name3] [reason] : [name1] et [name2] doivent tous [amount] à [name3] à cause de [reason]""",
                "multiple" : u"dette multiple [name1] [name2] [amount] [name3] [reason] : [name1] et [name2] doivent se partager la dette [amount] à payer à [name3] à cause de [reason]",
                "list" : u"dette list [name] : Liste les dettes de [name1]",
                "remove" : u"dette remove [id1], [id2], [id3] : Supprime les dettes dont les id sont [id1], [id2], [id3]"
                }
        SyncModule.__init__(self,
                            bot,
                            desc = desc,
                            command = "dette",
                            )

    @defaultcmd
    def answer(self, sender, message):
        return self.desc

    @answercmd("list")
    def list(self, sender, message):
        if message == "":
            tmp = self.bot.session.query(Dette).order_by(Dette.id).all()
            if tmp == []:
                return "Pas de dettes…"
            else:
                res = "\n " + 21*"_" + "\n"
                res += "| Toutes les Dettes : |\n"
                res += "|" + 21*"_" + "|" + 88*"_" + "\n"
                for elt in tmp:
                    res += u"| %s |\n" % elt
                res += "|" + 110*"_" + "|"
                return {"text": res, "monospace" : True}
        else:
            try:
                m = re.match(r"([^ ]+)(?: )*([^ ]+)*", message)
                name1 = m.group(1)
                name2 = m.group(2)
            except AttributeError:
                return "usage !dette list ou !dette list <name> ou !dette list <name1> <name2>"
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
                    return u"%s ne doit rien à personne" % (name1)
                else:
                    return u"%s ne doit rien à %s" % (name1, name2)
            res = ""

            if name2 is None:
                if p-n > 0:
                    res += u"%s doit encore recevoir %s € en tout\n" % (name1, str(p-n))
                else:
                    res += u"%s a un déficit de %s € en tout\n" % (name1, str(n-p))
                if n != 0:
                    res += " " + 12*"_" + "\n"
                    res += "| Dette(s) : |\n"
                    res += "|" + 12*"_" + "|" + 96*"_" + "\n"
                    res += res_debt
                    res += "|" + 109*"_" + "|\n"
                if p != 0:
                    res += " " + 13*"_" + "\n"
                    res += u"| Crédit(s) : |\n"
                    res += "|" + 13*"_" + "|" + 95*"_" + "\n"
                    res += res_credit
                    res += "|" + 109*"_" + "|\n"

            else:
                if p-n > 0:
                    res += u"%s doit recevoir %s € de %s\n" % (name1, str(p-n), name2)
                else:
                    res += u"%s doit %s € à %s\n" % (name1, str(n-p), name2)
                res += " " + 109*"_" + "\n"
                res += res_debt
                res += res_credit
                res += "|" + 109*"_" + "|\n"

            return {"text": res, "monospace" : True}

    @answercmd("add")
    def add(self, sender, message):
        try:
            m = re.match(r"([^ ]+(?: [^ ]+)*) ((?:\d+)(?:\.\d+)?) ([^ ]+) (.*)", message)
            debtor = m.group(1).split(' ')
            amount = m.group(2)
            creditor = m.group(3)
            reason = m.group(4)
        except AttributeError:
            return "usage : !dette add [name1] [amount] [name2] [reason] : Ajoute une dette de [amount] que doit payer [name1] à [name2] à cause de [reason]"
        res = ""
        for elt in debtor:
            if elt != creditor:
                dette = Dette(elt, amount, creditor, reason, time.time())
                self.bot.session.add(dette)
                self.bot.session.commit()
                sum_res = func.sum(Dette.amount)
                n = self.bot.session.query(sum_res).filter(and_(Dette.debtor == elt, Dette.creditor == creditor)).all()[0][0]
                p = self.bot.session.query(sum_res).filter(and_(Dette.debtor == creditor, Dette.creditor == elt)).all()[0][0]
                if n is not None and p is not None and (n-p) == 0:
                    deleted = self.bot.session.query(Dette).filter(or_(and_(Dette.debtor == elt, Dette.creditor == creditor), and_(Dette.debtor == creditor, Dette.creditor == elt))).all()
                    for e in deleted:
                        self.bot.session.delete(e)
                    self.bot.session.commit()
                    res += u"Les dettes entre %s et %s sont effacées\n" % (elt, creditor)
                else:
                    res += u"Ajout de la dette entre %s et %s\n" % (elt, creditor)
            else:
                res += u"On ne peut pas avoir une dette avec soi-même...\n"
        return res.rstrip()

    @answercmd("remove", "delete", "rm", "del")
    def remove(self, sender, message):
        if message == "":
            return "usage !dette remove id1,id2,id3,…"
        else:
            arg = message.split(",")
        res = []
        for i in arg:
            n = int(i)
            deleted = self.bot.session.query(Dette).filter(Dette.id == n).all()
            if deleted == []:
                res.append(u"Pas de dette d'id %s"%(n))
            else:
                self.bot.session.delete(deleted[0])
                res.append(u"%s a été supprimé"%(deleted[0]))
        self.bot.session.commit()
        return "\n".join(res)

    @answercmd("multiple")
    def multiple(self, sender, message):
        try:
            m = re.match(r"([^ ]+(?: [^ ]+)*) ((?:\d+)(?:\.\d+)?) ([^ ]+) (.*)", message)
            debtor = m.group(1).split(' ')
            amount = float(m.group(2))/float(len(debtor))
            creditor = m.group(3)
            reason = m.group(4)
        except AttributeError:
            return u"usage : dette multiple [name1] [name2] [amount] [name3] [reason] : [name1] et [name2] doivent se partager la dette [amount] à payer à [name3] à cause de [reason]"

        res = []
        for elt in debtor:
            if elt != creditor:
                dette = Dette(elt, amount, creditor, reason, time.time()) 
                self.bot.session.add(dette)
                self.bot.session.commit()
                sum_res = func.sum(Dette.amount)
                n = self.bot.session.query(sum_res).filter(and_(Dette.debtor == elt, Dette.creditor == creditor)).all()[0][0]
                p = self.bot.session.query(sum_res).filter(and_(Dette.debtor == creditor, Dette.creditor == elt)).all()[0][0]
                if n is not None and p is not None and (n-p) == 0:
                    deleted = self.bot.session.query(Dette).filter(or_(and_(Dette.debtor == elt, Dette.creditor == creditor), and_(Dette.debtor == creditor, Dette.creditor == elt))).all()
                    for e in deleted:
                        self.bot.session.delete(e)
                    self.bot.session.commit()
                    res.append(u"Les dettes entre %s et %s sont effacées" % (elt, creditor))
                else:
                    res.append(u"Ajout de la dette entre %s et %s" % (elt, creditor))
            else:
                res.append(u"On ne peut pas avoir une dette avec soi-même...\n")
        return "\n".join(res)


