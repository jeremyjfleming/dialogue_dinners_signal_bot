import os
from signalbot import SignalBot
from dialogue_dinners_signal_bot.service import DBService
from dialogue_dinners_signal_bot.cfl_commands import CFLCommands


if __name__ == "__main__":
    bot = SignalBot({
        "signal_service": os.environ["SIGNAL_SERVICE"],
        "phone_number": os.environ["PHONE_NUMBER"]
    })


    db_service = DBService()

    bot.register(CFLCommands(db_service), contacts=False, groups=['bot testing']) 
    bot.start()