#-*- coding: utf-8 -*-

from urllib import urlencode
from xmlrpclib import ServerProxy

from pipobot.lib.modules import SyncModule, defaultcmd, answercmd


class CmdDok(SyncModule):
    _config = (("user", str, None),
               ("password", str, None),
               ("url", str, None))

    def __init__(self, bot):
        desc = _("dok <query>: Search for <query> on the dokuwiki")
        self.server_proxy = ServerProxy(self.url + '/lib/exe/xmlrpc.php?' + urlencode({'u': self.user, 'p': self.password}))

        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="dok")

    @answercmd(r'(?P<query>.+)')
    def answer_query(self, sender, query):
        xml_search = self.server_proxy.dokuwiki.search(query)
        if query in [r['id'] for r in xml_search]:  # What about 'title' ?
            return self.url + query
        if len(xml_search) == 1:
            return self.url + xml_search[0]['id']
        if len(xml_search) > 1:
            return "\n".join([self.url + page['id'] for page in xml_search])
        return self.url + '?' + urlencode({'do': 'search', 'id': query})

    @defaultcmd
    def answer(self, sender, message):
        return self.desc
