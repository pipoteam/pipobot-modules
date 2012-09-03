#! /usr/bin/env python
#-*- coding: utf-8 -*-

from model import HlList, HlListMembers
from pipobot.lib.modules import SyncModule, defaultcmd, answercmd
from pipobot.lib.known_users import KnownUser


class HighLight(SyncModule):
    def __init__(self, bot):
        desc = _("hl <people>: Highligh <people> (whom can be registerd users, pseudos or list of people)")
        desc = _("\nhl <people> :<message>: Highligh <people>, and shows <message>")
        desc += _("\nhl show [<list>]: Shows <list> list of people (default: all)")
        desc += _("\nhl set <list> <people>: add <people> to <list>")
        #desc += _("\nhl rm <list> <people>: remove <people> from <list>")
        #desc += _("\nhl rm <list>: remove <list>")

        SyncModule.__init__(self,
                bot,
                desc=desc,
                command='hl')

    @answercmd(r'^show (?P<list>\w+)')
    def aswer_show(self, sender, message):
        hllist = self.bot.session.query(HlList).filter(HlList.name == message.group('list')).first()
        if not hllist:
            return _('I don\'t know that "%s" list' % message.group('list'))
        ret = _('list "%s"\'s members:' % message.group('list'))
        for user in hllist.members:
            ret += ' %s' % user.user
        return ret

    @answercmd(r'^show')
    def answer_showall(self, sender, message):
        ret = _("HighLigt Lists:")
        for hllist in self.bot.session.query(HlList).all():
            ret += "\n  %-31s" % hllist.name
            for user in hllist.members:
                ret += ' %s' % user.user
        return ret

    @answercmd(r'set')
    def answer_set(self, sender, message):
        ret = ''
        message = message.string.split(' ')
        if len(message) < 3:
            return _("%s: You must provide at least a list and a member" % sender)
        hllist = message[1]
        users = message[2:]
        knownusers = []
        unknownusers = []

        for user in users:
            knownuser = KnownUser.get(user, self.bot)
            if knownuser:
                knownusers.append(knownuser)
            else:
                unknownusers.append(user)

        if unknownusers:
            ret += _("\nunknown users: %s" % unknownusers)
        if not knownusers:
            ret += _("\n%s: You must provide at least one valid registered user" % sender)
            return ret.strip()

        hllistentry = self.bot.session.query(HlList).filter(HlList.name == hllist).first()
        if not hllistentry:
            hllistentry = HlList(hllist)
            self.bot.session.add(hllistentry)
            self.bot.session.commit()
            hllistentry = self.bot.session.query(HlList).filter(HlList.name == hllist).first()
            ret += _('\nlist "%s" added' % hllist)

        for user in knownusers:
            hllistmember = self.bot.session.query(HlListMembers).filter(HlListMembers.hllist_hlid == hllistentry.hlid).filter(HlListMembers.knownuser_kuid == user.kuid).first()
            if hllistmember:
                ret += _('\n"%s" is already in list "%s"' % (user, hllistentry))
            else:
                hllistmember = HlListMembers(hllistentry.hlid, user.kuid)
                self.bot.session.add(hllistmember)
                ret += _('\n"%s" added in list "%s"' % (user, hllistentry))

        self.bot.session.commit()
        return ret.strip()

    @defaultcmd
    def answer(self, sender, message):
        if not message:
            return self.desc
        knownusers = []
        unknownusers = []
        hllists = self.bot.session.query(HlList).all()
        hllistnames = []
        for hllist in hllists:
            hllistnames.append(hllist.name)
        ret = 'HL:'
        for user in message.split(':')[0].split(' '):
            if user in hllistnames:
                for hllist in hllists:
                    if hllist.name == user:
                        for knownuser in hllist.members:
                            knownusers.append(knownuser.user)
                        break
            else:
                knownuser = KnownUser.get(user, self.bot)
                if knownuser:
                    knownusers.append(knownuser)
                else:
                    unknownusers.append(user)
        for user in self.bot.occupants.users:
            if KnownUser.get(user, self.bot) in knownusers:
                ret += ' %s' % user
        for user in unknownusers:
            ret += ' %s' % user
        if ':' in message:
            ret += ' => ' + ':'.join(message.split(':')[1:]).strip()
        return ret
