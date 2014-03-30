# -*- coding: utf-8 -*-
import feedparser
import twitter
from .parser import get_id, get_time
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import FlushError
from sqlalchemy.exc import IntegrityError

from .model import Feed, Entry
from .metadata import Base


class Manager(object):
    __slots__ = ("bot", "db_session", "hooks")

    def __init__(self, db_path, bot):
        self.bot = bot
        engine = create_engine(db_path, convert_unicode=True)
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                                      autoflush=False,
                                                      bind=engine))
        Base.query = self.db_session.query_property()
        Base.metadata.create_all(bind=engine)


    def add_feed(self, url, name, twitter=False):
        if twitter:
            f = Feed(name, name, twitter=True)
        else:
            f = Feed(url, name)
        self.db_session.add(f)
        try:
            self.db_session.commit()
        except IntegrityError:
            self.db_session.rollback()
            return False
        self.update(silent=True, feed=name)
        return True

    def update(self, silent=False, feed=None):
        request = self.db_session.query(Feed)
        if feed is not None:
            request = request.filter(Feed.name == feed)
        result = request.all()

        for feed in result:
            if feed.twitter:
                api = twitter.Api()
                twits = api.GetUserTimeline(feed.name)
                for twit in twits:
                    # we discard answers to other twits
                    if not twit.in_reply_to_user_id:
                        txt = twit.GetText()
                        id = "%s_%s" % (feed.name, twit.GetId())
                        e = Entry(id, "", txt, "")
                        self.db_session.add(e)
                        feed.entries.append(e)
                        try:
                            self.db_session.commit()
                            if not silent:
                                msg = "[twitter: %s] %s" % (feed.name, txt)
                                self.bot.say(msg)
                        except (FlushError, IntegrityError):
                            self.db_session.rollback()

            else:
                parsed = feedparser.parse(feed.url)
                for entry in parsed.entries:
                    id = "%s_%s" % (feed.name, get_id(entry))
                    t = get_time(entry)
                    e = Entry(id, entry.link, t, entry.title)
                    self.db_session.add(e)
                    feed.entries.append(e)
                    try:
                        self.db_session.commit()
                        if not silent:
                            msg = "[%s] %s : %s" % (feed.name, entry.title, entry.link)
                            self.bot.say(msg)
                    except (FlushError, IntegrityError):
                        self.db_session.rollback()

    def add_entry(self, eid, url, date, title, feed):
        f = self.db_session.query(Feed).filter(Feed.name == feed).all()
        if f == []:
            raise
        else:
            feed = f[0]
            e = Entry(eid, url, date, title)
            self.db_session.add(e)
            feed.entries.append(e)
            self.db_session.add(feed)
        self.db_session.commit()

    def rm_feed(self, feed_name):
        feed = self.db_session.query(Feed).filter(Feed.name == feed_name).first()
        if feed:
            for entry in feed.entries:
                self.db_session.delete(entry)
            self.db_session.delete(feed)
            self.db_session.commit()
        return (feed is not None)

    def disable(self, feed_name):
        feed = self.db_session.query(Feed).filter(Feed.name == feed_name).first()
        if feed:
            feed.active = False
            self.db_session.add(feed)
            self.db_session.commit()
        return (feed is not None)

    def enable(self, feed_name):
        feed = self.db_session.query(Feed).filter(Feed.name == feed_name).first()
        if feed:
            feed.active = True
            self.db_session.add(feed)
            self.db_session.commit()
        return (feed is not None)

    def list_all(self):
        return self.db_session.query(Feed).all()
