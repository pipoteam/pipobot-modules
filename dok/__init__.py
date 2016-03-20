# -*- coding: utf-8 -*-

from urllib import urlencode
from xmlrpclib import ServerProxy

from pipobot.lib.modules import SyncModule, answercmd, defaultcmd


class CmdDok(SyncModule):
    _config = (("user", str, None),
               ("password", str, None),
               ("url", str, None))

    def __init__(self, bot):
        desc = _("dok <query>: Search for <query> on the dokuwiki")
        req_args = {'u': self.user, 'p': self.password}
        self.server_proxy = ServerProxy('%s/lib/exe/xmlrpc.php?%s' % (self.url, urlencode(req_args)))

        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="dok")

    @answercmd(r'(?P<query>.+)')
    def answer_query(self, sender, query):
        rtfd = _("Read The Fucking Dok: ")
        xml_search = self.server_proxy.dokuwiki.search(query)
        if query in [r['id'] for r in xml_search]:  # What about 'title' ?
            return rtfd + self.url + query
        if len(xml_search) == 1:
            return rtfd + self.url + xml_search[0]['id']
        if len(xml_search) > 1:
            return rtfd + "\n".join([self.url + page['id'] for page in xml_search])
        return rtfd + self.url + '?' + urlencode({'do': 'search', 'id': query})

    @defaultcmd
    def answer(self, sender, message):
        return self.desc
