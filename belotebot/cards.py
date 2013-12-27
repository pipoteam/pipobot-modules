#! /usr/bin/env python
#-*- coding: utf-8 -*-
""" Simple library for handling playing cards """

import random
UTF8 = True

class Suit :
    """ Class for handling suit  """

    name_suits = [(4, "P", "♠"), (3, "H", "♥"),(2, "C", "♦"),(1, "T", "♣")]

    def __init__(self, val, name, name_utf8) :
        """
            val      : value based on suit order (P>H>C>T)
            name     : string representation of the suit
            utf8     : utf8 representation of the suit
            trump    : is it trump suit ?
            dominant : is it asked suit ?
        """
        self.val = val
        self.name = name
        self.utf8 = name_utf8
        self.trump = False
        self.dominant = False

    def __cmp__(self, other) :
        if other is None :
            return 1
        else :
            return cmp(self.val, other.val)

    def __repr__(self) :
        return self.output()

    def output(self, utf8=UTF8) :
        """ Represent suit using utf8 or not"""
        if utf8 :
            return self.utf8
        else :
            return self.name

class Card :
    """ Class handling card """

    name_values     = ["7", "8", "9", "Valet", "Dame", "Roi", "10", "As"]
    ls_points       = [ 0 ,  0 ,  0 ,   2   ,    3   ,   4  ,  10 ,  11 ]
    ls_points_trump = [ 0 , 0 ,  14 ,  20   ,    3  ,    4 ,   10 ,  11 ]
    order_trump     = ["7", "8", "Dame", "Roi", "10", "As", "9", "Valet"]

    def __init__(self, val, suit, point=0,  point_trump=0) :
        """"
             val         : name of the card
             suit     : suit of the card
             point       : number of points earned for this card if not trump
             point_trump : number of points earned for this card if trump
        """
        self.val = val
        self.suit = suit
        self.point = point
        self.point_trump = point_trump

    def get_points(self) :
        """ Return number of points earned for this card """
        if self.suit.trump :
            return self.point_trump
        else :
            return self.point

    def __cmp__(self, other) :
        """ Compare 2 cards """

        if self.suit.trump :
            if other.suit.trump :
                return cmp(Card.order_trump.index(self.val), Card.order_trump.index(other.val)) # Best of two trumps
            else :
                return 1 # Trump win ("coupe")
        else :
            if other.suit.trump :
                return -1 # Trump win ("coupé")
            else :
                if self.suit == other.suit :
                    return cmp(Card.name_values.index(self.val), Card.name_values.index(other.val)) # Basic comparison
                else :
                    if self.suit.dominant :
                        return 1 # The other card is discarded
                    elif other.suit.dominant :
                        return -1 # This card is discarded
                    else :
                        return cmp(self.suit, other.suit) # The two cards are discarded, use the suit order

    def __eq__(self, other) :
        """ Check if two cards are the same """
        if other is None :
            return 1
        else :
            return self.val == other.val and self.suit == other.suit

    # Representation functions

    def __repr__(self) :
        return self.output()

    def output(self, utf8=UTF8) :
        """ Standart output """
        if utf8 :
            return "%s %s" % (self.val, self.suit.utf8)
        else :
            return "%s%s" % (self.val, self.suit.name)

            
class Deck :
    """ Class handling deck of cards """

    def __init__(self) :
        self.cards = []

        # Generate a deck of all cards
        self.suits = []
        self.assoc_suit = {} # Hash to associate suit representation to suit object
        self.assoc_suit_utf8 = {} # Hash to associate suit representation in utf8 to suit object

        for val, name_suit, name_suit_utf8 in Suit.name_suits :
            coul =  Suit(val, name_suit, name_suit_utf8)
            self.assoc_suit[name_suit.lower()] = coul
            self.assoc_suit_utf8[name_suit_utf8.lower()] = coul
            self.suits.append(coul)

        for _coul in self.suits :
            for name_valeur, point, point_trump in zip(Card.name_values, Card.ls_points, Card.ls_points_trump) :
                self.cards.append(Card(name_valeur, _coul, point, point_trump))

        # Hashes to associate card representations to card object
        self.assoc      = dict(list(zip([c.output(False).lower() for c in self.cards], self.cards)))
        self.assoc_utf8 = dict(list(zip([c.output(True).lower() for c in self.cards], self.cards)))

        # We shuffle it
        self.shuffle()

    def shuffle(self) :
        """ Shuffle the deck """
        random.shuffle(self.cards)

    def find(self, s_card) :
        """ Return card object via its representation """

        s_card = s_card.lower()
        try :
            return self.assoc[s_card]
        except KeyError :
            try :
                return self.assoc_utf8[s_card]
            except KeyError :
                return None

    def find_suit(self, s_coul) :
        """ Return suit object via its representation"""

        s_coul = s_coul.lower()
        try :
            return self.assoc_suit[s_coul]
        except KeyError :
            try :
                return self.assoc_suit_utf8[s_coul]
            except KeyError :
                return None
  
