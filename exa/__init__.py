#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request, urllib.parse
from pipobot.lib.modules import SyncModule, defaultcmd


class CmdExa(SyncModule):
    def __init__(self, bot):
        desc = "exa [mots clefs]\nEffectue une recherche sur le web et affiche les 4 premiers résultats"
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="exa",
                            )

    @defaultcmd
    def answer(self, sender, message):
        # Définir le nombre MAX de résultats à retourner
        limite = 4

        motclef = message
        motclef = motclef.encode("utf8")

        # Converti les mots clefs pour l'url
        valeurs = {'q': motclef}
        motclef = urllib.parse.urlencode(valeurs)
        url = 'http://exalead.fr/search/web/results/?' + motclef
        opener = urllib.request.build_opener()
        opener.addheaders = [('Accept-Language', 'fr')]
        result = opener.open(url)
        body = BeautifulSoup(result.read())

        # Verifie qu'on recupère bien des résultats
        try:
            nbre_results = len(body.find('ol', id="results").contents) / 2
        except:
            nbre_results = -1

        if nbre_results > 1:
            results = []
            for i in range(min([nbre_results, limite])):
                results.append(body.find('ol', id="results").contents[2 * i + 1].contents[3].contents[1].contents[1])
            # Fabrication de la sortie suivant le mode désiré
            redir = ""
            redir_xhtml = ""
            for i in range(min([nbre_results, limite])):
                redir += "\n " + results[i]['href'] + " --- " + results[i]['title']
                redir_xhtml += "\n<br/> <a href=\"" + results[i]['href'] + "\" alt=\"" + results[i]['href'] + "\">" + results[i]['title'] + "</a>"
        else:
            redir = "Pas de résultat"
            redir_xhtml = ""

        return {"text": redir, "xhtml": redir_xhtml}
