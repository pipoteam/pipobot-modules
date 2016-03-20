#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from pipobot.lib.modules import IQModule, SyncModule, answercmd, defaultcmd

import game
from cards import Deck


class CmdBelote(SyncModule):
    """ Module Belote for bot """

    def __init__(self, bot):
        desc = "Jeu de belote. Si vous voulez être renseigné, \
                allez au bureau des renseignements, ils vous renseigneront…"
        SyncModule.__init__(self, bot, desc=desc, name='b')
        self.game = None

    # Notify function for the belote game
    @staticmethod
    def html(card):
        """ HTMl output with img, not supported in all clients """
        ret = '<img src="http://www.bde.enseeiht.fr/~chataia/cards/png/%s%s.png" alt="%s" />'
        return ret % (card.val, card.suit.name, card.output())

    @staticmethod
    def bob(card):
        """" Output using BoB (Bits of binary, XEP-0231), supported in pidgin """
        return '<img src="cid:%s@bob.xmpp.org" alt="%s" />' % (card.output(utf8=False), card.output())

    def notify(self, msg, cards_obj=None, private=None):
        """ Implementation of a Belote() notify function:
                msg: Message with @ for cards
                cards_obj: object to replace with @
                private: if not None, name of the player to send
        """
        if cards_obj is not None:
            txtmsg = msg.replace('@', '%s') % tuple(cards_obj)
            htmlmsg = msg.replace('@', '%s %s') % \
                tuple((e for f in [(CmdBelote.html(c), CmdBelote.bob(c)) for c in cards_obj] for e in f))
            self.bot.say({'text': txtmsg, 'xhtml': htmlmsg}, priv=private)
        else:
            self.bot.say(msg, priv=private)

    def notify_cards(self):
        """ Default notify_cards """

        for player in self.game.players:
            self.notify('@ ' * len(player.cards), sorted(player.cards), private=player)

    def notify_tapis(self):
        """ Show the table """
        pass

    @answercmd("cartes")
    def show_cards(self, sender):
        """ A player ask to show his cards """
        player = self.game.find_player(sender)
        self.notify('@ ' * len(player.cards), sorted(player.cards), private=player)

    @answercmd("tapis")
    def show_tapis(self, sender):
        self.notify_tapis()

    @answercmd("init")
    def init_game(self, sender):
        """ Init new game """

        self.game = game.Belote(self.notify, self.notify_cards, self.notify_tapis)

    @defaultcmd
    def answer(self, sender, message):
        """ Default answer if not an answercmd """

        if self.game.state == 'wait_player' and 'moi' in message:
            self.game.join(sender)
        elif self.game.state in ['wait_choice', 'sec_choice']:
            suit = self.game.deck.find_suit(message.decode('utf8'))
            take = suit is not None or message == 'y'
            self.game.choice(sender, take=take, suit=suit)
        elif self.game.state == 'wait_play':
            card = self.game.deck.find(message.decode('utf8'))
            if card is None:
                self.notify("Cette carte n'existe pas")
                return
            self.game.play(sender, card)


class IqBobBelote(IQModule):

    def __init__(self, bot):
        IQModule.__init__(self, bot, name='BoBCard', desc='BoB for belote cards')
        bot.registerPlugin("xep_0231")

        # Generate cache
        deck = Deck()
        for card in deck.cards:
            path = os.path.join(os.path.dirname(__file__), "png/%s.png" % card.output(utf8=False))
            cid = card.output(utf8=False) + "@bob.xmpp.org"

            fdimg = open(path)
            raw_img = fdimg.read()
            fdimg.close()

            bot.plugin['xep_0231'].set_bob(data=raw_img, mtype='image/png', cid=cid)
