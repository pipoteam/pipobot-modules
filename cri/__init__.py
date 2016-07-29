from pipobot.lib.modules import ListenModule


class CriAnswer(ListenModule):
    def __init__(self, bot):
        desc = "Pipo crie"
        ListenModule.__init__(self, bot, name="crianswer", desc=desc)

    def answer(self, sender, message):
        message = message.upper()
        if 'CRI' in message:
            return message.split('CRI', 1)[1]
