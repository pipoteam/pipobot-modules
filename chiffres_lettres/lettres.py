# -*- coding: utf-8 -*-
""" Tools to start and resolve 'le mot le plus long' game """
import logging
import os
import random

logger = logging.getLogger("pipobot.lettres")


def creation_dictionnaire_ordonne(dico):
    """ Reads DICO_FILE and create a python dictionary
        out of it """
    try:
        with open(dico, "r") as fichier_dico:
            dict_ord_len = {}
            for longueur in range(26):
                dict_ord_len[longueur + 1] = []
            while True:
                mot = fichier_dico.readline()
                if mot == '':
                    break
                mot = mot.strip('\n')
                if '-' in mot:
                    mot = mot.replace('-', '')
                dict_ord_len[len(mot)].append(mot)
            fichier_dico.close()
            return dict_ord_len
    except IOError:
        return None


def trouver_mot_plus_long(longueur_max_mot, dico, tirage):
    """ Finds the longest word in 'dico' using letters of 'tirage' """
    longueur_mot = longueur_max_mot
    solution = []
    set_tirage = set(tirage)
    while longueur_mot > 0:
        for mot in dico[longueur_mot]:
            if set(mot).issubset(set_tirage):
                tirage_test = list(tirage)
                try:
                    for lettre in mot:
                        tirage_test.remove(lettre)
                except ValueError:
                    continue
                solution.append(mot)
        if solution != []:
            return solution
        longueur_mot -= 1


class Lettres:
    """ Class to define the game 'le mot le plus long' """
    _config = (("dico", str, None),)

    def __init__(self, dico):
        self.result = []
        self.letters = []
        self.tirage()
        if dico != "":
            dict_ord_len = creation_dictionnaire_ordonne(dico)
            if dict_ord_len is not None:
                self.dict_ord_len = dict_ord_len

    def solve(self):
        """ Finds the best solution for the game """
        if hasattr(self, "dict_ord_len"):
            solution = trouver_mot_plus_long(len(self.letters),
                                             self.dict_ord_len,
                                             self.letters)
            return solution
        else:
            return None

    def tirage(self):
        """ Initialize the game with random letters """
        self.letters = []
        consonnes = 'bcdfghjklmnpqrstvwxz'
        voyelles = 'aeiouy'

        for _ in range(9):
            if random.randint(0, 1) == 0:
                self.letters += random.choice(voyelles)
            else:
                self.letters += random.choice(consonnes)
        self.letters = sorted(self.letters)
