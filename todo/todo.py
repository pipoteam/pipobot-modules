# -*- coding: utf-8 -*-
import re
import time

from pipobot.lib.module_test import ModuleTest, string_gen
from pipobot.lib.modules import SyncModule, answercmd

from model import Todo


class CmdTodo(SyncModule):
    """ Gestion de TODO-lists """
    def __init__(self, bot):
        desc = {"": "Gestion des TODO-lists",
                "list": """todo list : affiche la liste des todolist existantes.
todo list [name] : affiche les todo de la liste [name]""",
                "add": "todo add [name] [msg] : crée le nouveau todo [msg] dans la liste [name]",
                "remove/delete/rm": "todo remove [n,...] : supprime les todos d'id [n,...]",
                "search": "todo search [element]: recherche un TODO qui contient [element]",
                }
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="todo")

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

    @answercmd("(remove|delete|rm) (?P<ids>(\d+,? ?)+)")
    def remove(self, sender, ids):
        send = ""
        for i in re.split('[ ,]+', ids):
            n = int(i)
            deleted = self.bot.session.query(Todo).filter(Todo.id == n).all()
            if deleted == []:
                send += "Pas de todo d'id %s\n" % n
            else:
                self.bot.session.delete(deleted[0])
                send += "%s a été supprimé\n" % deleted[0]
        self.bot.session.commit()
        return send[0:-1]

#########################################################################################################
#                       UNIT TEST                                                                       #
#########################################################################################################


class TodoAdd(ModuleTest):
    def test_todo_add(self):
        """ !todo add """
        self.todo_list = string_gen(8)
        self.todo_msg = string_gen(50)
        bot_rep = self.bot_answer("!todo add %s %s" % (self.todo_list, self.todo_msg))
        self.assertEqual(bot_rep, u"TODO ajouté")

    def tearDown(self):
        """ In case of failure, we manually remove the todo we added """
        remove = self.bot.session.query(Todo).filter(Todo.content.like("%" + self.todo_msg + "%")).first()
        if remove is not None:
            self.bot.session.delete(remove)
            self.bot.session.commit()


class TodoRemove(ModuleTest):
    def setUp(self):
        """ Creates 3 random todo we add manually to the database """
        self.todos = []
        todos = {string_gen(8): string_gen(50),
                 string_gen(8): string_gen(50),
                 string_gen(8): string_gen(50)}
        for list_name, todo in todos.iteritems():
            todo = Todo(list_name, todo, "sender", time.time())
            self.bot.session.add(todo)
            self.bot.session.commit()
            self.todos.append(todo)

    def test_todo_remove(self):
        """ !todo remove """
        bot_rep = self.bot_answer("!todo remove %s" % ",".join([str(elt.id) for elt in self.todos]))
        expected = "\n".join(["%s a été supprimé" % todo for todo in self.todos])
        self.assertEqual(bot_rep, expected)

    def tearDown(self):
        """ In case of failure, we manually remove the todo we added """
        for todo in self.todos:
            remove = self.bot.session.query(Todo).filter(Todo.id == todo.id).first()
            if remove is not None:
                self.bot.session.delete(remove)
                self.bot.session.commit()


class TodoSearch(ModuleTest):
    def setUp(self):
        """ Creates a random todo we add manually to the database """
        todo_list = string_gen(8)
        todo_msg = string_gen(50)
        self.todo = Todo(todo_list, todo_msg, "sender", time.time())
        self.bot.session.add(self.todo)
        self.bot.session.commit()

    def test_search(self):
        """ !todo search """
        bot_rep = self.bot_answer("!todo search %s" % self.todo.content)
        expected = str(self.todo)
        self.assertEqual(bot_rep, expected)

    def tearDown(self):
        """ We manually remove the todo we added """
        remove = self.bot.session.query(Todo).filter(Todo.id == self.todo.id).first()
        self.bot.session.delete(remove)
        self.bot.session.commit()
