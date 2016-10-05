# -*- coding: utf-8 -*-

from pipobot.lib.modules import AsyncModule, Pasteque
from pipobot.lib.utils import unescape
from twython import Twython, TwythonError

from .model import LastTweets, Tweets

RT = 'retweeted_status'
REPLY_NAME = 'in_reply_to_screen_name'
REPLY_TWEET = 'in_reply_to_status_id_str'


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
        self.err = False
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
            try:
                timeline = self.twitter.get_user_timeline(screen_name=user)
            except TwythonError as err:
                if self.err:
                    raise Pasteque("TWITTER IS DOWN OMG OMG OMG\n%s" % err)
                self.err = True
                return
            self.err = False
            for tweet in timeline:
                if tweet['id'] <= last_tweet.last:
                    break
                if say and not (self.avoid_rt and RT in tweet and already_said(tweet[RT]['id'])):
                    text = tweet['text']
                    if RT in tweet:
                        fmt = u'Tweet de %s retweeté par %s: ' % (tweet[RT][u'user'][u'screen_name'], user)
                        text = tweet[RT]['text']
                    elif REPLY_NAME in tweet and tweet[REPLY_NAME] is not None:
                        fmt = u'Tweet de %s en réponse à https://twitter.com/%s/status/%s : '
                        fmt %= (user, tweet[REPLY_NAME], tweet[REPLY_TWEET])
                    else:
                        fmt = u'Tweet de %s: ' % user
                    self.bot.say({'text': fmt + unescape(text),
                                  'xhtml': fmt + Twython.html_for_tweet(tweet)})
                tweets.add(tweet['id'])
            if timeline:
                last_tweet.last = timeline[0]['id']
        for tweet in tweets:
            self.bot.session.merge(Tweets(id=tweet))
        self.bot.session.commit()
