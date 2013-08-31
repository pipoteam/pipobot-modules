#! /usr/bin/env python
#-*- coding: utf-8 -*-
""" Define belote game"""

import random
from cards import Deck, Card

class Belote(object) :
    """" Defines a belote game, as a state machine """

    def __init__(self, notify_cb=None, notify_cards=None, notify_table=None) :
        # Game is implemented as a state machine, each state is associated to a method
        # 4 external transitions are defined : start, new_player, choice, play
        self.states = { 'init'       : self.init,         # initialize game for example deck
                        'wait_player': self.wait_player,  # wait for 4 four players, and create them
                        'init_choice': self.init_choice,  # 1st  turn, distribute cards and announce top card
                        'wait_choice': self.wait_choice,  # wait for player choice (take the card or not)
                        'sec_choice' : self.sec_choice,   # in case of a second choice turn
                        'init_game'  : self.init_game,    # choice has been made, distribute the rest
                        'init_trick' : self.init_trick,    # initialize a new trick
                        'wait_play'  : self.wait_play,    # wait for players to play
                        'end_trick'  : self.end_trick,     # all the players have played
                        'end_game'   : self.end_game,     # all cards have been played
                      }
        self.state = None

        self.notify       = notify_cb if notify_cb is not None else self.notify_def
        self.notify_cards = notify_cards if notify_cards is not None else self.notify_defcards
        self.notify_table = notify_table if notify_table is not None else self.notify_deftable

        # Game attribute
        self.deck = None
        self.players = []
        self.teams = ()
        self.propos = None
        self.bidder = None
        self.player_idx = 0

        # Trick attribute
        self.trick = None
        self.trump_suit = None
        self.dominant = None
        self.players_ord = None
        self.trick_winner = None

        self.set_state('init')

    def set_state(self, new_state) :
        """ Change state """

        #print "new state : %s" % new_state
        self.state = new_state
        self.states[new_state]()


    #
    # State implementation
    #

    def init(self) :
        """ Initialize game for example deck """
        self.players = []
        self.teams = ()
        self.notify(u"Partie démarrée, qui veut jouer ?")
        self.set_state('wait_player')

    def wait_player(self) :
        """ Basically do nothing, wait for players to self.join() """
        if len(self.players) == 4 :
            # Shuffle to determine teams
            random.shuffle(self.players)
            # Reset new id with new order
            for i, j in enumerate(self.players):
                j.id = i
            # Creation of teams and go forward in the game (choice turn)
            self.teams = Team(self.players[::2]), Team(self.players[1::2])
            self.notify(u"Les équipes : %s contre %s"% self.teams)
            self.set_state('init_choice')

    def init_choice(self) :
        """ Draw 5 first cards each and propose card"""

        self.deck = Deck()
        self.player_idx = 0 # Current player
        self.bidder = None
        self.trump_suit = None
        for player in self.players :
            player.cards = []

        self.notify_table()

        for j in self.players :
            for _ in range(5) :
                j.cards.append(self.deck.cards.pop())

        self.propos = self.deck.cards.pop()
        self.notify(u"Carte proposée : @", (self.propos,))
        self.notify_cards()
        self.set_state('wait_choice')

    def wait_choice(self) :
        """ Wait for player choice, do nothing, all work will be done with choice """
        
        if self.player_idx == 4:
            # All players said no, second turn
            self.player_idx = 0
            self.notify("Second tour !")
            self.set_state('sec_choice')
        else :
            self.notify(u"À %s de parler" % self.players[self.player_idx])

    def sec_choice(self) :
        """ Wait for player choice, do nothing, all work will be done with choice """

        if self.player_idx == 4:
            # All players said no, end of the game
            self.player_idx = 0
            self.set_state('init_choice')
        else :
            self.notify(u"À %s de parler" % self.players[self.player_idx])

    def init_game(self) :
        """ Distribute the rest of cards, assume self.bidder and self.trump_suit defined """
        
        self.notify(u"%s a pris, atout %s" % (self.bidder, self.trump_suit))
        # Set trump flag on cards
        for suit in self.deck.suits :
            suit.trump = False
        self.trump_suit.trump = True

        self.bidder.cards.append(self.propos)

        for j in self.players :
            for _ in range(2 if j == self.bidder else 3) :
                j.cards.append(self.deck.cards.pop())
        
        self.player_idx = 0 # First player plays first

        self.set_state('init_trick')

    def init_trick(self) :
        """ ... """

        self.trick = [] # Cards played on this trick
        self.dominant = None # Dominant suit

        # Temporary order of players with first player
        self.players_ord = self.players[self.player_idx:] + self.players[0:self.player_idx]

        self.notify_cards()

        self.set_state('wait_play')

    def wait_play(self) :
        """ Wait for player to play, do nothing, all work will be done with play() """

        if len(self.trick) == 4 :
            self.set_state('end_trick')
        else :
            self.notify(u"C'est au tour de %s" % self.players[self.player_idx])

    def end_trick(self) :
        """ End of the trick, update score """

        self.trick_winner = self.players_ord[self.trick.index(max(self.trick))]
        self.trick_winner.team.score += sum([card.get_points() for card in self.trick])
        
        self.player_idx = self.trick_winner.id

        self.notify("%s remporte le pli" % self.trick_winner)
        if len(self.players[0].cards) != 0 :
            self.set_state('init_trick')
        else :
            self.set_state('end_game')
    
    def end_game(self) :
        """ End of game, final score and stuff """

        self.trick_winner.team.score += 10
        
        loosers, winners = sorted(self.teams, key=lambda x: x.score)

        if winners.score == loosers.score :
            self.notify(u"Litige")
        elif self.bidder.team == winners :
            self.notify(u"Elle est faite")
        else :
            self.notify(u"Elle est dedans")
            if self.bidder.team.belote :
                self.notify(u"Et en plus la belote est perdue mouahahahah")
                loosers.score -= 20
                winners.score += 20

        if loosers.score == 0 or loosers.score == 20 and loosers.belote :
            self.notify(u"Capot !!!!")

        # Show scores
        self.notify(u"Scores : ")
        for team in self.teams :
            self.notify(u"%s : %d" % (team, team.score))
         
        self.notify(u"Vainqueurs : %s" % winners)
        self.set_state('init_choice')

    #
    # External actions
    #
    def find_player(self, player_s) :
        """ Simple wrapper to transform string to player via name """

        for player in self.players :
            if player.name == player_s :
                return player
        return None

    def join(self, player_s) :
        """ External action when a player join """

        if self.state != 'wait_player' :
            self.notify(u"Partie en cours")
            return

        if self.find_player(player_s) is None :
            player = Player(len(self.players), player_s)
            self.players.append(player)
            self.notify(u"%s est dans la partie" % player.name)
            self.set_state('wait_player')


    def choice(self, player_s, take, suit=None) :
        """ External action when a player choose wether or not he takes """

        player = self.find_player(player_s)

        if self.state != 'wait_choice' and self.state != 'sec_choice':
            self.notify(u"Pas un tour de demande")
            return

        if player != self.players[self.player_idx] :
            self.notify(u"Pas à ton tour de parler")
            return

        if take :
            if self.state == 'wait_choice' :
                self.trump_suit = self.propos.suit
            if self.state == 'sec_choice' :
                if suit is None:
                    self.notify(u"On choisit un couleur au deuxième tour")
                    self.set_state(self.state)
                    return
                if suit == self.propos.suit :
                    self.notify(u"Nope, fallait prendre au premier tour !")
                    self.set_state(self.state)
                    return
                self.trump_suit = suit
            self.bidder = player
            self.set_state('init_game')
            return
        else :
            # Said no, next player
            self.player_idx += 1
            self.set_state(self.state)
            return

    def play(self, player_s, card) :
        """ External action when a player plays a card """
        
        player = self.find_player(player_s)

        if self.state != 'wait_play' :
            self.notify(u"Pas un tour de jeu")
            return

        if player != self.players[self.player_idx] :
            self.notify(u"Pas à ton tour de parler")
            return

        if card not in player.cards :
            self.notify(u"Ben t'as pas cette carte -_-")
            return False
        
        if self.trick == [] :
            # First card of the trick, its suit becomes dominant
            self.dominant = card.suit
            for suit in self.deck.suits :
                suit.dominant = False
            card.suit.dominant = True
        else :
            if card.suit != self.dominant :
                partner_win = self.players_ord[self.trick.index(max(self.trick))] in player.team.members
                for _ca in player.cards :
                    # Must play dominant if we have some
                    if _ca.suit == self.dominant :
                        self.notify(u"TTTttt, on fournit quand on peut")
                        return False
                for _ca in player.cards :
                    # Must use a trump except partner is winning
                    if not card.suit.trump and _ca.suit.trump and not partner_win :
                        self.notify(u"Vous êtes obligé de couper")
                        return False
            if card.suit.trump :
                # Must overtrump
                for _ca in self.trick :
                    if _ca.suit.trump and _ca > card :
                        for _ca2 in player.cards :
                            if _ca2.suit.trump and _ca2 > _ca :
                                self.notify(u"On doit monter à l'atout")
                                return False
        # Play the card
        self.notify(u"%s joue @" % player, (card,))
        self.trick.append(card)
        player.cards.remove(card)
        
        #Belote, Rebelote ?
        if card.suit.trump and  (\
            ( card.val == "Dame" and Card("Roi",card.suit) in player.cards) \
         or ( card.val == "Roi" and Card("Dame",card.suit) in player.cards)) :
            self.notify(u"Belote !")
            player.team.belote = True
            player.team.score += 20
        elif card.suit.trump and card.val in ['Dame','Roi'] and player.team.belote :
            self.notify(u"Rebelote !")

        # Next player
        self.player_idx = (self.player_idx + 1)%4
        self.set_state('wait_play')
        return True

    #
    # Default notify action
    #


    def notify_def(self, msg, cards_obj=None, private=None) :
        """ Example prototype for a notify function:
                msg: Message with @ for cards
                cards_obj: object to replace with @
                private: if not None, name of the player to send
        """
        if cards_obj is not None :
            msg = msg.replace('@','%s') % tuple(cards_obj)
        if private :
            msg = "%s: %s" % (private.name, msg)
        print msg

    def notify_defcards(self) :
        """ Default notify_cards """

        for player in self.players :
            self.notify('@ '*len(player.cards), player.cards, private=player)

    def notify_deftable(self) :
        """ Default notify_table """

        self.notify(' '.join([plyr.name for plyr in self.players]))

class Player(object) :
    """ Define a player """
    def __init__(self, _id, name) :
        self._id   = _id   # Id of the player
        self.name  = name  # Name of the player
        self.cards = []    # Cards in hand
        self.team  = None  # Player's team

    def __repr__(self) :
        return self.name

class Team :
    """ Define a team """

    def __init__(self, members) :
        self.members = members
        self.score   = 0
        self.belote  = False
        for member in self.members :
            member.team = self

    def __repr__(self) :
        return  u" et ".join([str(m) for m in self.members])


if __name__ == '__main__' :
    def main() :
        """ Little main game for testing purpose """

        bel = Belote()
        bel.join("alice")
        bel.join("bob")
        bel.join("charles")
        bel.join("dede")
        while True :
            command = raw_input("> ")
            try :
                if command == "" :
                    continue

                if command[0] == "p" :
                    _, player, card = command.split(' ', 2)
                    try :
                        card = bel.deck.find(card.decode('utf8'))
                    except KeyError:
                        print "Carte existe pas"
                        continue
                    bel.play(player, card)

                if command[0] == "c" :
                    _, joueur, choice = command.split(' ', 2)
                    suit = bel.deck.find_suit(choice.decode('utf8'))
                    take = suit is not None or choice == 'y'
#                print joueur, take, suit
                    bel.choice(joueur, take=take, suit=suit)
            except ValueError :
                pass
    main()
