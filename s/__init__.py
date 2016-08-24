from pipobot.lib.known_users import KnownUser
from pipobot.lib.modules import SyncModule, answercmd, defaultcmd

from last_words.model import LastWords


class SModule(SyncModule):
    def __init__(self, bot):
        desc = _("!s /<from>/<to>/ : Correct <from> in your last message by <to>\n")
        desc += _("!s /<from>/<to>/ <someone> : Correct <from> in <someone> last message by <to>")
        SyncModule.__init__(self, bot, desc=desc, name="s")

    @defaultcmd
    def answer_help(self, sender, message):
        if message:
            return self.desc

    @answercmd(r'^/(?P<before>.*)/(?P<after>.*)/(?P<guy>.*)$')
    def answer_with_guy(self, sender, before, after, guy):
        return self.answer(sender, before, after, guy.strip() or sender)

    @answercmd(r'^/(?P<before>.*)/(?P<after>.*)$')
    def answer_without_guy(self, sender, before, after):
        return self.answer(sender, before, after, sender)

    def answer(self, sender, before, after, guy):
        user = KnownUser.get(guy, self.bot)
        if not user:
            return _("I don't know %s, please try '!user register'." % guy)
        last_words = self.bot.session.query(LastWords).filter(LastWords.kuid == user.kuid).first()
        if last_words is None:
            return _("I don't know %s's last message" % user.get_pseudo())
        if before not in last_words.message:
            return _("%s is not in %s's last message" % (before, user.get_pseudo()))
        ret = _("%s meant to say: %s") % (user.get_pseudo(), last_words.message.replace(before, after))
        if sender != guy:
            ret = _("%s thinks " % sender) + ret
        return ret
