#-*- coding: utf8 -*-
import urllib
import re
from pipobot.lib.modules import SyncModule, defaultcmd


class CmdText2Ascii(SyncModule):
    def __init__(self, bot):
        desc = u"!t2a texte : transforme le texte en ascii art"
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="t2a")

    @defaultcmd
    def answer(self, sender, message):
        if message == '':
            return self.desc
        else:
            text = self.replace_accent(message)
            url = 'http://www.network-science.de/ascii/ascii.php?TEXT=%s&x=32&y=13&FONT=ogre&RICH=no&FORM=left&STRE=no&WIDT=80' % text
            f = urllib.urlopen(url)
            content = f.read()
            f.close()

            matched = re.search(r'<PRE>.*?</PRE>.*?<PRE>(.*?)</PRE>', content, re.DOTALL)
            if matched:
                asc = matched.group(1)
                asc = asc.rstrip(' \t\n\r')
                if not re.match("^( )+\n.*", asc, re.DOTALL):
                    asc = "\n" + asc
                asc = asc.replace('&quot;', '"')
                return {"text": asc, "monospace": True}

    def replace_accent(self, text):
        to_replace = { 'a': ['à', 'â', 'ä'],
                    'e': ['é', 'è', 'ê', 'ë'],
                    'i': ['î', 'ï'],
                    'u': ['ù', 'ü', 'û'],
                    'o': ['ô', 'ö'],
                    'c': ['ç'],
                    'ae': ['æ'],
                    'A': ['Â', 'Ä', 'À'],
                    'E': ['Ê', 'Ë', 'É', 'È'],
                    'I': ['Ï', 'Î'],
                    'U': ['Û', 'Ü', 'Ù'],
                    'O': ['Ô', 'Ö'],
                    'C': ['Ç'],
                    'AE': ['Æ'],
                    ' ': ['\'']}
        for (ch, wrong_ch) in to_replace.iteritems():
            for w_ch in wrong_ch:
                text = text.replace(w_ch, ch)
        return text
