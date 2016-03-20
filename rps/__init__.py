# -*- coding: utf-8 -*-
import random

from pipobot.lib.module_test import ModuleTest
from pipobot.lib.modules import SyncModule, answercmd, defaultcmd


class CmdRPS(SyncModule):
    def __init__(self, bot):
        desc = """Rock Paper Scissors:
rps init <n> : lance une nouvelle partie avec <n> joueurs
rps bot : pour se mesurer au bot !!!
rps (Rock|Paper|Scissor) : pour jouer"""
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="rps")
        self.choices = ["Rock", "Paper", "Scissors"]
        self.players = 0
        self.manche = {}
        self.bot.rps = self

    @answercmd("init (?P<n>\d+)")
    def init(self, sender, n):
        try:
            if int(n) > len(self.bot.occupants.users):
                return "Not enough players in the room"
            self.players = int(n)
            self.manche = {}
            return "Game initialized with %d players" % (self.players)
        except (ValueError, IndexError):
            return "You should see the man…"

    @answercmd("bot")
    def bot_play(self, sender):
        self.manche[self.bot.name] = random.choice(self.choices)
        left = self.players - len(self.manche.keys())
        if left == 0:
            res = self.results()
            self.players = 0
            self.manche = {}
            msgs = [{"text": "I've played !", "nopriv": True}, {"text": res, "nopriv": True}]
            return msgs
        elif left == 1:
            return {"text": "I have played, only %s answer is expected. Come on!" % left,
                    "nopriv": True}
        else:
            return {"text": "I have played, %s answers are expected" % left,
                    "nopriv": True}

    @answercmd("(?P<play>Rock|Paper|Scissor)")
    def default(self, sender, play):
        if play in self.choices:
            if sender in self.manche.keys():
                l = ["You must be stupid.", "What else?!"]
                return "You have already played... " + random.choice(l)
            elif self.players == 0:
                return "There is no game launched"
            else:
                self.manche[sender] = play
                left = self.players - len(self.manche.keys())
                if left == 0:
                    l = ["%s: You were very looooooooooong to answer..." % sender,
                         "%s: You are the last and perhaps the least!" % sender,
                         "%s has finally played." % sender]
                    msgs = [{"text": random.choice(l), "nopriv": True}]
                    res = self.results()
                    self.players = 0
                    self.manche = {}
                    msgs += [{"text": res, "nopriv": True}]
                elif left == 1:
                    msgs = {"text": "%s has played, only %s answer is expected. Come on !" % (sender, left),
                            "nopriv": True}
                else:
                    msgs = {"text": "%s has played, %s answers are expected." % (sender, left),
                            "nopriv": True}
                return msgs

    @staticmethod
    def beats(choice1, choice2):
        return (choice1 == "Paper" and choice2 == "Rock") \
            or (choice1 == "Scissors" and choice2 == "Paper") \
            or (choice1 == "Rock" and choice2 == "Scissors")

    def results(self):
        res = {}
        ret = ""
        for player, pchoice in self.manche.iteritems():
            loose = False
            for opponent, ochoice in self.manche.iteritems():
                if opponent != player:
                    if CmdRPS.beats(ochoice, pchoice):
                        loose = True
                        break
            res[player] = loose
        else:
            resultats = ", ".join(["%s: %s" % (player, score) for player, score in self.manche.iteritems()])
            ret = ", ".join(["%s" % (player) for player, status in res.iteritems() if not status])
            plural = "s" if ret.count(",") != 0 else ""
            return "Results: %s, Winner%s: %s" % (resultats, plural, ret)


class RpsTest(ModuleTest):
    users = ["alice", "bob"]

    def setUp(self):
        for user in self.users:
            self.bot.occupants.add_user(user,
                                        "%s@domain.tdl" % user,
                                        "participant")

    def tearDown(self):
        for user in self.users:
            self.bot.occupants.rm_user(user)

    def test_game_users(self):
        bot_rep = self.bot_answer("!rps init 2", user="alice")
        self.assertEqual(bot_rep, "Game initialized with 2 players")

        bot_rep = self.bot_answer("!rps Rock", user="alice")
        self.assertEqual(bot_rep, "alice has played, only 1 answer is expected. Come on !")

        bot_rep = self.bot_answer("!rps Paper", user="bob")
        # The first line of the answer is a random message: we do not care what it is…
        self.assertEqual(bot_rep.partition("\n")[2],
                         "Results: bob: Paper, alice: Rock, Winner: bob")

    def test_draw(self):
        bot_rep = self.bot_answer("!rps init 2", user="alice")
        self.assertEqual(bot_rep, "Game initialized with 2 players")

        bot_rep = self.bot_answer("!rps Rock", user="alice")
        self.assertEqual(bot_rep, "alice has played, only 1 answer is expected. Come on !")

        bot_rep = self.bot_answer("!rps Rock", user="bob")
        # The first line of the answer is a random message: we do not care what it is…
        self.assertEqual(bot_rep.partition("\n")[2],
                         "Results: bob: Rock, alice: Rock, Winners: bob, alice")

    def test_play_with_bot(self):
        bot_rep = self.bot_answer("!rps init 2", user="alice")
        self.assertEqual(bot_rep, "Game initialized with 2 players")

        bot_rep = self.bot_answer("!rps Rock", user="alice")
        self.assertEqual(bot_rep, "alice has played, only 1 answer is expected. Come on !")

        bot_rep = self.bot_answer("!rps bot", user="alice").split("\n")
        self.assertEqual(bot_rep[0], "I've played !")

        expected = "Results: alice: Rock, %s: (Rock|Paper|Scissors), Winner(s?): .*"
        expected %= (self.bot.name)
        self.assertRegexpMatches(bot_rep[1], expected)
