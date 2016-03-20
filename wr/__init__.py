# -*- coding: utf-8 -*-

from pipobot.lib.module_test import ModuleTest
from pipobot.lib.modules import SyncModule, answercmd

import wrapi


class CmdWordRef(SyncModule):
    def __init__(self, bot):
        desc = _("wr in out expression: traduit [expression] de la langue [in] vers la langue [out]")
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="wr")
        self.wordref = wrapi.WordRef()

    @answercmd("lang")
    def langs(self, sender):
        return ", ".join(wrapi.LANGS)

    @answercmd("(?P<in_lang>\w{2}) (?P<out_lang>\w{2}) (?P<req>.*)")
    def translate(self, sender, in_lang, out_lang, req):
        try:
            rep = self.wordref.translate(in_lang, out_lang, req)
            result = u"\n".join(map(unicode, rep.principal))
            return result if result != u"" else u"Aucune traduction trouvée pour %s" % req
        except wrapi.NoTranslation:
            return u"Aucune traduction trouvée pour %s" % req
        except wrapi.APIAuth:
            return u"Erreur lors de l'accès à wordreference (contacter l'administrateur du bot !)"
        except wrapi.InternalError:
            return u"Erreur lors de l'accès à wordreference"
        except wrapi.LangError as e:
            return unicode(e)
