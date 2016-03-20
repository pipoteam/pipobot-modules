# -*- coding: UTF-8 -*-

import os
from random import choice

from pendu_ascii import asc_res


class Pendu(object):
    def __init__(self, word):
        self.setword(word)

    def setword(self, word):
        self._word = word
        self.played = ["_"] * len(word)
        self.letters = set()
        self.okletters = set()
        self.maxanswers = 8

    def getword(self):
        return self._word

    word = property(getword, setword)

    def playedtostr(self):
        return u"Lettres jouées: %s" % ", ".join(sorted(self.letters | self.okletters))

    def propose(self, letter):
        res = ""
        if letter in (self.letters | self.okletters):
            return u"Lettre déjà proposée"

        if letter in self.word:
            i = -1
            for l in self.word:
                i += 1
                if l == letter:
                    self.played[i] = self.word[i]
                    self.okletters.add(letter)
            res = u"Bien vu !"
            if self.solved():
                res += u"\nEt oui, le mot à trouver était bien %s !" % self.word
                self.word = ""
            else:
                res += u" Mot actuel: %s" % "".join(self.played)
        else:
            if len(self.letters) == self.maxanswers:
                res = asc_res[8]
                res += u"Tu devais trouver %s" % self.word
                self.word = ""
            else:
                self.letters.add(letter)
                res = asc_res[len(self.letters) - 1]
                res += "\nMot actuel : %s" % ("".join(self.played))
        return res

    def solved(self):
        return not ("_" in self.played)

    def create_word(self, word_file):
        word_list = []
        with open(word_file) as f:
            for line in f:
                word_list.append(line.strip().lower())
        return choice(word_list)

if __name__ == "__main__":
    g = Pendu("pipo")
    print g.played
    print g.propose("p")
    print g.playedtostr()
    print g.solved()
    print g.propose("r")
    print g.playedtostr()
    print g.solved()
    print g.propose("i")
    print g.playedtostr()
    print g.solved()
    print g.propose("o")
