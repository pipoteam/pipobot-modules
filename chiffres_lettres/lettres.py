# -*- coding: utf-8 -*-
""" Tools to start and resolve 'le mot le plus long' game """
import os
import random

DICO_FILE = os.path.join(os.path.dirname(__file__), 'ods3')


def creation_dictionnaire_ordonne():
    """ Reads DICO_FILE and create a python dictionary
        out of it """
    with open(DICO_FILE, "r") as fichier_dico:
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
    def __init__(self):
        self.result = []
        self.letters = []
        self.tirage()
        self.dict_ord_len = creation_dictionnaire_ordonne()

    def solve(self):
        """ Finds the best solution for the game """
        solution = trouver_mot_plus_long(len(self.letters),
                                         self.dict_ord_len,
                                         self.letters)
        return solution

    def tirage(self):
        """ Initialize the game with random letters """
        consonnes = 'bcdfghjklmnpqrstvwxz'
        voyelles = 'aeiouy'

        for _ in range(9):
            if random.randint(0, 1) == 0:
                self.letters += random.choice(voyelles)
            else:
                self.letters += random.choice(consonnes)
        self.letters = sorted(self.letters)
