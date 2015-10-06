# -*- coding: utf-8 -*-
import re
import sqlalchemy.exc
from pipobot.lib.modules import ListenModule
from pipobot.lib.utils import check_url
from pipobot.lib.known_users import KnownUser
from model import RepostUrl

try:
    from hyperlinks_scanner import HyperlinksScanner
except ImportError:
    HyperlinksScanner = None


URLS_RE = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-/_=?:;]|[!*\(\),~@]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


class CmdUrl(ListenModule):
    _config = (("repost", bool, False), ("repost_ignore", list, []))

    def __init__(self, bot):
        desc = "Extracting title of page from URL"
        ListenModule.__init__(self, bot, name="url", desc=desc)

    def answer(self, sender, message):
        if HyperlinksScanner:
            scanner = HyperlinksScanner(message, strict=True)
            urls = set([link.url for link in scanner])
        else:
            urls = set(URLS_RE.findall(message))

        try:
            repost_msg = self.check_repost(sender, urls)
        except sqlalchemy.exc.OperationalError:
            self.bot.session.rollback()
            repost_msg = []
        except sqlalchemy.exc.InvalidRequestError:
            repost_msg = []

        title_page = self.get_title(urls)
        send = repost_msg + title_page
        return None if send == [] else "\n".join(send)

    def check_repost(self, sender, urls):
        send = []
        if self.repost:
            for url in urls:
                if not any(i in url for i in self.repost_ignore):
                    res = self.bot.session.query(RepostUrl).filter(RepostUrl.url == url).first()
                    if res:
                        send.append('OLD! ')
                        first = KnownUser.get_antihl(res.jid, self.bot)
                        first_date = 'le ' + res.date.strftime('%x') + ' à ' + res.date.strftime('%X')
                        first_date = first_date.decode("utf-8")
                        if res.count == 1:
                            send.append(u'Ce lien a déjà été posté %s par %s sur %s…' % (first_date, first, res.chan))
                        else:
                            send.append(u'Ce lien a déjà été posté %s fois depuis que %s l’a découvert, %s, sur %s…' % (res.count, first, first_date, res.chan))
                        res.count += 1
                    else:
                        u = RepostUrl(url,
                                      self.bot.occupants.pseudo_to_jid(sender),
                                      self.bot.chatname)
                        self.bot.session.add(u)
                        self.bot.session.commit()
        return send

    def get_title(self, urls):
        send = []
        for url in urls:
            send += check_url(url)
        return send
