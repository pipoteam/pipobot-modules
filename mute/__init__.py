#-*- coding: utf-8 -*-
import xmpp
import random
import pipobot.lib.utils
from threading import Timer
from pipobot.lib.modules import SyncModule, defaultcmd


class CmdMute(SyncModule):
    def __init__(self, bot):
        desc = "mute [nom]\n[nom] ne peut plus parler sur le salon !!!"
        SyncModule.__init__(self,
                            bot,
                            name="mute",
                            pm_allowed=False,
                            desc=desc)

    def restore(self, name):
        pipobot.lib.utils.unmute(name, self.bot)

    @defaultcmd
    def answer(self, sender, message):
        role_sender = self.bot.occupants.pseudo_to_role(sender)
        reasonfail = ["%s: TPPT !!!",
                      "%s: Je n'obéis qu'au personnel compétent",
                      "%s: Tu crois vraiment que je vais t'obéir",
                      "%s: Non mais tu te crois où ? oO",
                      "%s: J'vais l'dire aux modérateurs"]
        reasonkick = ["TU TE TAIS %s",
                      "Désolé %s, je ne fais qu'obéir aux ordres"]

        lst = message.split(" ")
        rapport = ""
        if len(lst) == 2:
            if lst[0] == "undo":
                who = lst[1]
                pipobot.lib.utils.unmute(who, self.bot)
                return "%s peut maintenant parler" % who

        for muted in lst:
            authorised = False
            orNot = False
            if muted == self.bot.name:
                rapport += "Je vais pas me virer moi-même oO\n"
                continue
            jidmuted = self.bot.occupants.pseudo_to_jid(muted)
            jidsender = self.bot.occupants.pseudo_to_jid(sender)
            if jidmuted == "":
                rapport += "%s n'est pas dans le salon\n" % muted
                continue
            if jidmuted == jidsender:
                if muted == sender:
                    rapport += "Tu veux te muter toi-même ?\n"
            elif role_sender != "moderator":
                orNot = True
                authorised = True
                toMute = sender
                rapport += "%s n'a pas le droit de muter %s\n" % (sender, muted)
            else:
                authorised = True
                toMute = muted
                rapport += "J'ai muté %s pour toi !\n" % muted

            if authorised:
                if self.bot.occupants.pseudo_to_role(toMute) == "moderator":
                    rapport = "On ne peut pas muter quelqu'un ayant des droits aussi élevés\n"
                else:
                    t = Timer(30.0, lambda name=toMute: self.restore(name))
                    t.start()
                    if orNot:
                        pipobot.lib.utils.mute(toMute,
                                               random.choice(reasonfail) % toMute,
                                               self.bot)
                    else:
                        pipobot.lib.utils.mute(toMute,
                                               random.choice(reasonkick) % toMute,
                                               self.bot)
        return rapport.rstrip()
