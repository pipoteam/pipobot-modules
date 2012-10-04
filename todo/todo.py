#! /usr/bin/python2
# -*- coding: utf-8 -*-
import time
from pipobot.lib.modules import SyncModule, answercmd
from model import Todo


class CmdTodo(SyncModule):
    """ Gestion de TODO-lists """
    def __init__(self, bot):
        desc = {"": "Gestion des TODO-lists",
                "list": """todo list : affiche la liste des todolist existantes.
todo list [name] : affiche les todo de la liste [name]""",
                "add": "todo add [name] [msg] : crée le nouveau todo [msg] dans la liste [name]",
                "remove": "todo remove [n,...] : supprime les todos d'id [n,...]",
                "search": "todo search [element]: recherche un TODO qui contient [element]",
                }
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            command="todo")

    @answercmd("list", "list (?P<listname>\S+)")
    def list(self, sender, listname=""):
        if listname == "":
            tmp = self.bot.session.query(Todo).group_by(Todo.name).all()
            if tmp == []:
                return "Pas de todolist…"
            else:
                return "Toutes les TODO-lists: \n%s" % ("\n".join([todo.name for todo in tmp]))
        else:
            if listname == "all":
                tmp = self.bot.session.query(Todo).order_by(Todo.name).all()
                llistname = ""
                send = "\n"
                for elt in tmp:
                    if elt.name != llistname:
                        send += "%s: \n" % (elt.name)
                        llistname = elt.name
                    send += "\t%s \n" % elt
            else:
                tmp = self.bot.session.query(Todo).filter(Todo.name == listname).all()
                if tmp == []:
                    send = ""
                else:
                    send = u"%s :\n%s" % (listname, "\n".join(map(unicode, tmp)))
            if send.strip() == "":
                return "TODO-list vide"
            return send

    @answercmd("add (?P<liste>\S+) (?P<msg>.*)")
    def add(self, sender, liste, msg):
        if liste == "all":
            return "On ne peut pas nommer une liste 'all'"
        todo = Todo(liste, msg, sender, time.time())
        self.bot.session.add(todo)
        self.bot.session.commit()
        return "TODO ajouté"

    @answercmd("search (?P<query>.*)")
    def search(self, sender, query):
        found = self.bot.session.query(Todo).filter(Todo.content.like("%" + query + "%"))
        return "\n".join(map(str, found))

    @answercmd("(remove|delete) (?P<ids>(\d+,?)+)")
    def remove(self, sender, ids):
        send = ""
        for i in ids.split(','):
            n = int(i)
            deleted = self.bot.session.query(Todo).filter(Todo.id == n).all()
            if deleted == []:
                send += "Pas de todo d'id %s\n" % n
            else:
                self.bot.session.delete(deleted[0])
                send += "%s a été supprimé\n" % deleted[0]
        self.bot.session.commit()
        return send[0:-1]
