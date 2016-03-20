from pipobot.lib.modules import AsyncModule
from twython import Twython

from .model import LastTweets, Tweets

RT = 'retweeted_status'


class Twitter(AsyncModule):
    """A module to follow tweets form some users"""
    _config = (("users", list, []), ("app_key", str, ""), ("app_secret", str, ""),
               ("avoid_rt", bool, True), ("shy_start", bool, True))

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
        if self.shy_start:
            self.action(say=False)

    def action(self, say=True):
        tweets = set()

        def already_said(id):
            if id in tweets:
                return True
            tweets.add(id)
            q = self.bot.session.query(Tweets).filter(Tweets.id == id)
            return self.bot.session.query(q.exists()).scalar()

        for user in self.users:
            last_tweet = self.bot.session.query(LastTweets).filter(LastTweets.user == user).first()
            timeline = self.twitter.get_user_timeline(screen_name=user)
            if timeline[0]['id'] > last_tweet.last:
                for tweet in timeline:
                    if tweet['id'] <= last_tweet.last:
                        break
                    if say and not (self.avoid_rt and RT in tweet and already_said(tweet[RT]['id'])):
                        self.bot.say(u'Tweet de %s: %s' % (user, tweet['text']))
                    tweets.add(tweet['id'])
                last_tweet.last = timeline[0]['id']
        for tweet in tweets - set(t[0] for t in self.bot.session.query(LastTweets.last).all()):
            self.bot.session.add(Tweets(id=tweet))
        self.bot.session.commit()
