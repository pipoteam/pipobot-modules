#! /usr/bin/env python
#-*- coding: utf-8 -*-

from model import HlList
from pipobot.lib.modules import SyncModule, defaultcmd, answercmd
from pipobot.lib.known_users import KnownUser, minpermlvl


class HighLight(SyncModule):
    def __init__(self, bot):
        desc = _("hl <people>: Highligh <people> (whom can be registerd users, pseudos or list of people)")
        desc += _("\nhl <people> :<message>: Highligh <people>, and shows <message>")
        desc += _("\nhl show : Shows list of people")
        desc += _("\nhl set <list> <people>: Add <people> to <list>")
        desc += _("\nhl rm <list> <people>: Remove <people> from <list>")
        desc += _("\nhl rm <list>: Remove <list>")

        SyncModule.__init__(self,
                bot,
                desc=desc,
                command='hl')

    @answercmd(r'show (?P<plist>\w+)')
    def aswer_show(self, sender, plist):
        hllist = self.bot.session.query(HlList).filter(HlList.name == plist).first()
        if not hllist:
            return _('I don\'t know that "%s" list' % plist)
        ret = _('list "%s"\'s members:' % plist)
        ret += ", ".join(map(str, hllist.members))
        return ret

    @answercmd(r'show')
    def answer_showall(self, sender):
        hllists = self.bot.session.query(HlList).all()
        if not hllists:
            return _("%s: There is no HighLight List… Maybe you can create one, before trying that ?" % sender)
        ret = _("HighLight Lists:")
        for hllist in hllists:
            ret += "\n  %-31s" % hllist.name
            ret += ", ".join(map(str, hllist.members))
        return ret

    @answercmd(r'^set (?P<hllist>\w+) (?P<users>.*)')
    def answer_set(self, sender, hllist, users):
        ret = ''
        knownusers = []
        unknownusers = []
        users = users.strip().split()

        # We first check if users in the input users list are valid or not
        for user in users:
            knownuser = KnownUser.get(user, self.bot, authviapseudo=True, in_live=False)
            if knownuser is not None:
                knownusers.append(knownuser)
            else:
                unknownusers.append(user)

        # If there are some invalid users
        if unknownusers:
            ret += _("\nunknown users: %s" % " ".join(unknownusers))

        # If we have no valid user to add
        if not knownusers:
            ret += _("\n%s: You must provide at least one valid registered user" % sender)
            return ret.strip()

        # Now we must add all knownusers to the hllist


        hllistentry = self.bot.session.query(HlList).filter(HlList.name == hllist).first()

        # If the hllist does not exist, we create it
        if not hllistentry:
            hllistentry = HlList(hllist)
            self.bot.session.add(hllistentry)
            ret += _('\nlist "%s" created' % hllist)
            self.bot.session.commit()

        # Then we add all knownusers to the list
        for user in knownusers:
            if user in hllistentry.members:
                ret += _('\n"%s" is already in list "%s"' % (user, hllistentry))
            else:
                hllistentry.members.append(user)
                self.bot.session.commit()
                ret += _('\n"%s" added in list "%s"' % (user, hllistentry))

        self.bot.session.commit()
        return ret.strip()

    @answercmd(r'rm (?P<hllist>\w+)', r'rm (?P<hllist>\w+) (?P<users>.*)')
    @minpermlvl(2)
    def answer_rm(self, sender, hllist, users=""):
        ret = ''
        # We search for the list <hllist>
        hllist = self.bot.session.query(HlList).filter(HlList.name == hllist).first()

        # If the list does not exist
        if not hllist:
            return _("%s: There is no such HighLight List" % sender)

        users = users.strip().split()
        # If we want to remove users from the list
        if users:
            for user in users:
                # We search the knownuser associated to the username "user"
                knownuser = KnownUser.get(user, self.bot, authviapseudo=True, in_live=True)
                # If there is no result
                if not knownuser:
                    ret += _('user "%s" is not even registered…\n' % user)
                # if the user is not in the list
                elif not knownuser in hllist.members:
                    ret += _('user "%s" is not a member of this list\n' % knownuser)
                    continue
                #if the user is in the list
                else:
                    hllist.members.delete(knownuser)
                    ret += _('user "%s" has been deleted from list "%s"\n' % (knownuser, hllist))
        # We remove the list
        else:
            self.bot.session.delte(hllist)
            ret += _('list "%s" has been deleted' % hllistname)

        self.bot.session.commit()
        return ret.strip()

    @defaultcmd
    def answer(self, sender, message):
        # !hl some people (: some messages)
        if not message:
            return self.desc

        knownusers = []
        unknownusers = []
        hllistnames = []
        hllists = self.bot.session.query(HlList).all()
        for hllist in hllists:
            hllistnames.append(hllist.name)
        ret = 'HL:'
        user_list, message = message.partition(":")[::2]
        for user in user_list.split():
            if user in hllistnames:
                for hllist in hllists:
                    if hllist.name == user:
                        knownusers.extend(hllist.members)
                        break
            else:
                knownuser = KnownUser.get(user, self.bot, authviapseudo=True, in_live=True)
                if knownuser:
                    knownusers.append(knownuser)
                else:
                    unknownusers.append(user)

        for user in self.bot.occupants.users:
            if KnownUser.get(user, self.bot, authviapseudo=True, in_live=True) in knownusers:
                ret += ' %s ' % user
        ret += " ".join(unknownusers)

        if message.strip():
            ret += u' → ' + message.strip()
        return ret
