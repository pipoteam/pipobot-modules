# -*- coding: utf-8 -*-
import os
import random
import time
from string import ascii_lowercase
from itertools import combinations

DICO_FILE = os.path.join(os.path.dirname(__file__), 'ods3')

def creation_dictionnaire_ordonne():
    with open(DICO_FILE, "r") as fichier_dico:
        dict_ord_len = {}
        for longueur in range(26):
            dict_ord_len[longueur+1] = []
        while True:
            mot = fichier_dico.readline()
            if mot == '':
                break
            mot = mot.strip('\n')
            if '-' in mot:
                mot = mot.replace('-','')
            dict_ord_len[len(mot)].append(mot)
        fichier_dico.close()
        return dict_ord_len


def trouver_mot_plus_long(longueur_max_mot, dico, tirage):
    longueur_mot = longueur_max_mot
    solution= []
    set_tirage = set(tirage)
    while longueur_mot > 0:
        for mot in dico[longueur_mot]:
            if set(mot).issubset(set_tirage) :
                tirage_test = list(tirage)
                try:
                    for lettre in mot:
                        tirage_test.remove(lettre)
                except:
                    continue
                solution.append(mot)
        if solution != []:
            return solution
        longueur_mot -= 1

class Lettres:
    def __init__(self):
        self.result = []
        self.tirage()
        self.dict_ord_len = creation_dictionnaire_ordonne()

    def solve(self):
        solution = trouver_mot_plus_long(len(self.letters), self.dict_ord_len, self.letters)
        return solution

    def tirage(self):
        self.letters = []
        consonnes = 'bcdfghjklmnpqrstvwxz'
        voyelles = 'aeiouy'

        for i in range(9):
            if random.randint(0, 1) == 0:
               self.letters += random.choice(voyelles)
            else:
                self.letters += random.choice(consonnes)
        self.letters = sorted(self.letters)
