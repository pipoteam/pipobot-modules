from pipobot.lib.known_users import KnownUser
from pipobot.lib.modules import ListenModule

from .model import LastWords


class LastWordsModule(ListenModule):
    """A module to log users' last words"""

    def __init__(self, bot):
        ListenModule.__init__(self, bot, name="last_words", desc="Logs last words")

    def answer(self, sender, message):
        user = KnownUser.get(sender, self.bot)
        if user:
            last_words = self.bot.session.query(LastWords).filter(LastWords.kuid == user.kuid).first()
            if last_words is None:
                last_words = LastWords(kuid=user.kuid)
            last_words.message = message
            self.bot.session.add(last_words)
            self.bot.session.commit()
