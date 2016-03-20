# -*- coding: utf-8 -*-
import random

import pipobot.lib.utils
from pipobot.lib.modules import SyncModule, defaultcmd


class CmdKick(SyncModule):
    def __init__(self, bot):
        desc = "kick [nom]\nKick quelqu'un du salon !"
        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="kick",
                            pm_allowed=False
                            )

    @defaultcmd
    def answer(self, sender, message):
        role_sender = self.bot.occupants.pseudo_to_role(sender)
        reasonfail = [u"%s: TPPT !!!",
                      u"%s: Je n'obéis qu'au personnel compétent",
                      u"%s: Tu crois vraiment que je vais t'obéir",
                      u"%s: Non mais tu te crois où ? oO",
                      u"%s: J'vais l'dire aux modérateurs"]
        reasonkick = [u"Au revoir %s",
                      u"Désolé %s, je ne fais qu'obéir aux ordres"]

        lst = message.split(" ")
        rapport = []
        for kicked in lst:
            authorised = False
            or_not = False
            if kicked == self.bot.name:
                rapport.append(u"Je vais pas me virer moi-même oO")
                to_kick = sender
                or_not = True
                authorised = True
            jidkicked = self.bot.occupants.pseudo_to_jid(kicked)
            if jidkicked == "":
                rapport.append(u"%s n'est pas dans le salon" % kicked)
                continue
            jidsender = self.bot.occupants.pseudo_to_jid(sender)
            if jidkicked == jidsender:
                if kicked == sender:
                    rapport.append(u"Tu veux te virer toi-même ?")
                else:
                    authorised = True
                    to_kick = kicked
                    ret = u"J'ai viré %s à la demande de %s car il semblerait que ce soit un imposteur"
                    rapport.append(ret % (kicked, sender))
            elif role_sender != "moderator":
                or_not = True
                authorised = True
                to_kick = sender
                rapport.append(u"%s n'a pas le droit de virer %s" % (sender, kicked))
            else:
                authorised = True
                to_kick = kicked
                rapport.append(u"J'ai viré %s pour toi !" % kicked)

            if authorised:
                if self.bot.occupants.pseudo_to_role(to_kick) == "moderator":
                    rapport.append(u"On ne peut pas kicker quelqu'un ayant des droits aussi élevés")
                else:
                    if or_not:
                        pipobot.lib.utils.kick(to_kick,
                                               random.choice(reasonfail) % to_kick, self.bot)
                    else:
                        pipobot.lib.utils.kick(to_kick,
                                               random.choice(reasonkick) % to_kick, self.bot)
        return "\n".join(rapport)
