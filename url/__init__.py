# -*- coding: utf-8 -*-
import re
from datetime import timedelta, datetime

import sqlalchemy.exc
from pipobot.lib.known_users import KnownUser
from pipobot.lib.modules import ListenModule
from pipobot.lib.utils import check_url

from model import RepostUrl

try:
    from hyperlinks_scanner import HyperlinksScanner
except ImportError:
    HyperlinksScanner = None


URLS_RE = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-/_=?:;]|[!*\(\),~@]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


class CmdUrl(ListenModule):
    # repost_ignore_delay is the number of seconds to wait between two
    # submissions of the same url before prompting that this is an old message.
    _config = (("repost", bool, False), ("repost_ignore", list, []),
            ("repost_ignore_delay", int, 60))

    def __init__(self, bot):
        desc = "Extracting title of page from URL"
        ListenModule.__init__(self, bot, name="url", desc=desc)

    def answer(self, sender, message):
        if HyperlinksScanner:
            scanner = HyperlinksScanner(message, strict=True)
            urls = set([link.url for link in scanner])
        else:
            urls = set(URLS_RE.findall(message))

        # We cannot iter by number on sets, because of their intrinsic structure
        urls = list(urls)

        title_page = self.get_title(urls)

        try:
            repost_msg = self.check_repost(sender, urls, title_page)
        except sqlalchemy.exc.OperationalError:
            self.bot.session.rollback()
            repost_msg = []
        except sqlalchemy.exc.InvalidRequestError:
            repost_msg = []

        send = repost_msg + title_page
        return None if send == [] else "\n".join(send)

    def check_repost(self, sender, urls, titles):
        if not self.repost:
            return []
        send = []
        for i in range(0, len(urls)):
            url = urls[i]
            # the conversion to unicode is quite important to prevent sqlite conversion errors between 8-bytestrings and UTF-8 sqlite3 values
            title_page = unicode(titles[i])
            if not any(k in url for k in self.repost_ignore):
                res = self.bot.session.query(RepostUrl).filter(RepostUrl.url == url).first()
                if res:
                    # Do not send a message if the link was shared less than repost_ignore_delay
                    # seconds ago or the page title changed since its submission
                    if (datetime.now() - res.last_date) > timedelta(seconds=self.repost_ignore_delay) and title_page == res.title:
                        send.append('OLD! ')
                        first = KnownUser.get_antihl(res.jid, self.bot)
                        first_date = 'le ' + res.date.strftime('%x') + ' à ' + res.date.strftime('%X')
                        first_date = first_date.decode("utf-8")
                        if res.count == 1:
                            send.append(u'Ce lien a déjà été posté %s par %s sur %s…' % (first_date, first, first.chan))
                        else:
                            ret = u'Ce lien a déjà été posté %s fois depuis que %s l’a découvert, %s, sur %s…'
                            send.append(ret % (res.count, first, first_date, res.chan))
                    res.title = title_page
                    res.count += 1
                    # Update the time someone posted the link
                    res.last_date = datetime.now()
                else:
                    u = RepostUrl(url,
                                  self.bot.occupants.pseudo_to_jid(sender),
                                  self.bot.chatname,
                                  title_page)
                    self.bot.session.add(u)
                    self.bot.session.commit()
        return send

    def get_title(self, urls):
        send = []
        for url in urls:
            send += check_url(url)
        return send
