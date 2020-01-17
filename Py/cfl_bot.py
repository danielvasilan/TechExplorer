
class CflParser:
    REPLY_PREFFIX = "[Cashflow-op] "
    botName = "(no name)"
    
    def __init__(self, name):
        self.botName = name

    def reply(self, replyText):
        print(self.REPLY_PREFFIX + replyText)

    def parseLine(self, lineText):
        if lineText.upper().startswith(self.botName.upper()):
            self.reply(lineText)
        else:
            print(lineText)

    def cflAddExpense(self, date, category, amount):
        self.reply ("Add expense")


bot = CflParser("Gogu")
bot.parseLine("Gogu test")
bot.parseLine("no-op test")

