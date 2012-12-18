#-*- coding: utf-8 -*-
import random
import threading
import time
from pipobot.lib.modules import SyncModule, answercmd, defaultcmd
from pipobot.lib.module_test import ModuleTest


choices = ["Rock", "Paper", "Scissors", "Lizard", "Spock"]
delay = 15
victory = {("Paper", "Rock"): "covers",
           ("Scissors", "Paper"): "cuts",
           ("Rock", "Lizard"):  "crushes",
           ("Lizard", "Spock"): "poisons",
           ("Spock", "Scissors"): "smashes",
           ("Scissors", "Lizard"): "decapitates",
           ("Lizard", "Paper"): "eats",
           ("Paper", "Spock"): "disproves",
           ("Spock", "Rock"): "vaporizes",
           ("Rock", "Scissors"): "crushes"}


class Player(object):
    __slots__ = ("name", "ready", "choice")

    def __init__(self, name, ready=True):
        self.name = name
        self.ready = ready
        self.choice = None


class CmdRPSLS(SyncModule):
    def __init__(self, bot):
        desc = """Rock Paper Scissors Lizard Spock:
rpsls init <someone> : Pour défier quelqu'un.
rpsls accept <someone> : Accèpte le défi de quelqu'un.
rpsls (Rock|Paper|Scissor|Lizard|Spock) : pour jouer"""
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="rpsls")
        self.p1 = None
        self.p2 = None
        self.running = False

    @answercmd("init (?P<who>\S+)")
    def init(self, sender, who):
        self.p1 = None
        self.p2 = None
        if who == self.bot.name:
            self.p1 = Player(sender)
            self.p2 = Player(self.bot.name)
            self.p2.choice = random.choice(choices)
            self.thread = threading.Thread(target=self.wait_for_it)
            self.thread.start()
            return u"%s: OK je veux bien t'affronter !" % sender
        elif who == sender:
            return u"%s: Euh, tu ne peux pas jouer contre toi-même" % sender
        else:
            self.p1 = Player(sender)
            self.p2 = Player(who, ready=False)
            return u"%s: %s te provoque en duel !" % (who, sender)

    @answercmd("accept (?P<who>\S+)")
    def accept(self, sender, who):
        if self.p1 is None or self.p2 is None:
            return u"Il faut lancer un défi avant d'accepter !"

        if self.p1.name == who and self.p2.name == sender:
            self.p2.ready = True
            self.thread = threading.Thread(target=self.wait_for_it)
            self.thread.start()
            ret = u"Partie lancée entre %s et %s\n" % (self.p1.name, self.p2.name)
            ret += u"Vous avez maintenant %s secondes pour jouer" % delay
            return ret
        else:
            if self.p1.name != who:
                return u"%s: %s ne t'a pas défié… pour jouer contre lui: !rpsls init" % (sender, who)
            else:
                return u"%s: Tu n'as pas le droit de participer à cette partie !" % sender

    def wait_for_it(self):
        self.running = True
        cpt = 0
        while self.running and cpt < delay:
            cpt += 1
            time.sleep(1)
        if self.running:
            res = "STOOOOOOP - "
        else:
            res = ""
        res += self.beats()
        self.p1 = None
        self.p2 = None
        self.bot.say(res)

    @answercmd("(?P<play>Rock|Paper|Scissor|Lizard|Spock)")
    def default(self, sender, play):
        if self.p1 is None or self.p2 is None:
            return u"Aucune partie lancée"
        elif not (self.p1.ready and self.p2.ready):
            return u"On se calme, y'a des gens qui ne sont pas prêts !"

        if self.p1.name == sender:
            user = self.p1
            other = self.p2
        elif self.p2.name == sender:
            user = self.p2
            other = self.p1
        else:
            return u"%s: tu n'as pas le droit de jouer !" % sender

        if user.choice is not None:
            return u"%s: tu as déjà joué !" % sender
        else:
            user.choice = play
            if other.choice is not None:
                self.running = False
            return u"%s: merci d'avoir joué !" % sender

    def beats(self):
        if self.p1 is None or self.p2 is None:
            return u"Aucune partie lancée"

        if self.p1.choice is None and self.p2.choice is None:
            return u"Aucun des deux joueurs n'a joué…"
        elif self.p1.choice is None:
            return u"%s a oublié de jouer, %s a gagné !" % (self.p1.name, self.p2.name)
        elif self.p2.choice is None:
            return u"%s a oublié de jouer, %s a gagné !" % (self.p2.name, self.p1.name)

        #If we are here: both players have played
        if self.p1.choice == self.p2.choice:
            return u"%s et %s sont a égalité" % (self.p1.name, self.p2.name)

        if (self.p1.choice, self.p2.choice) in victory:
            win = self.p1
            lost = self.p2
        else:
            win = self.p2
            lost = self.p1
        return u"%s %s %s : %s a gagné !!!" % (win.choice, victory[(win.choice, lost.choice)], lost.choice, win.name)
