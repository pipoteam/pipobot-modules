from pipobot.lib.modules import AsyncModule

from twython import Twython

from .model import LastTweets


class Twitter(AsyncModule):
    """A module to follow tweets form some users"""
    _config = (("users", list, []), ("app_key", str, ""), ("app_secret", str, ""))

    def __init__(self, bot):
        AsyncModule.__init__(self,
                             bot,
                             name="twitter",
                             desc="Displays tweets",
                             delay=60)

        for user in self.users:
            last = self.bot.session.query(LastTweets).order_by(LastTweets.last.desc()).first()
            last_id = last.last if last is not None else 0
            if not self.bot.session.query(LastTweets).filter(LastTweets.user == user).first():
                self.bot.session.add(LastTweets(user=user, last=last_id))
                self.bot.session.commit()

        token = Twython(self.app_key, self.app_secret, oauth_version=2).obtain_access_token()
        self.twitter = Twython(self.app_key, access_token=token)

    def action(self):
        for user in self.users:
            last_tweet = self.bot.session.query(LastTweets).filter(LastTweets.user == user).first()
            timeline = self.twitter.get_user_timeline(screen_name=user)
            if timeline[0]['id'] > last_tweet.last:
                for tweet in timeline:
                    if tweet['id'] <= last_tweet.last:
                        break
                    self.bot.say(u'Tweet de %s: %s' % (user, tweet['text']))
                last_tweet.last = timeline[0]['id']
                self.bot.session.commit()
