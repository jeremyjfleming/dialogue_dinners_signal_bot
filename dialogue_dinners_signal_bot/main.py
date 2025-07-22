import os
from signalbot import SignalBot, Command, Context
from sqlalchemy import create_engine
from dialogue_dinners_signal_bot.db_schema import Base
from dialogue_dinners_signal_bot.service import DBService


class CFLCommands(Command):



    def __init__(self, db_service):
        super().__init__()
        self.db_service = db_service
    
    async def _list_pairs(self, pairs, c: Context):
        response = "Pairs:"
        list_pairs = []
        pos_index = len(response)-1
        for key, pair in enumerate(pairs):
            response += "\nAB" # filler characters for the mentions
            pos_index += 2
            list_pairs.append({"author": pair[0], "start": pos_index, "length": 1})     
            list_pairs.append({"author": pair[1], "start": pos_index+1, "length": 1})
            pos_index += 1

        await c.send(response, None, list_pairs)

    async def handle(self, c: Context):
    

        if c.message.text.startswith("!dd"):
            command = c.message.text.split(" ")[1].strip().lower()
            if command == "test":
                await c.send("Pairings are working!")
            elif command == "poll":
                await c.send("If you are interested in participating in dialogue dinners this semester, please react below.")
            elif command == "add":
                user_list = c.message.mentions
                self.db_service.add(user_list)
                await c.send("Users added")
            elif command == "pairs":
                # List current pairings
                pairs = self.db_service.get_pairings()
                if pairs:
                    await self._list_pairs(pairs, c)
                else:
                    await c.send("Failed to list pairs or no active pairings found.")
            elif command == "generate":
                # Generate pairings
                pairs = self.db_service.generate()
                if pairs:
                    self._list_pairs(pairs, c)  
                else:
                    await c.send("Failed to generate pairs or no pairs to generate!")
            elif command == "complete":
                # Complete a pairing
                user_list = c.message.mentions 
                if self.db_service.complete(user_list[1], user_list[2]):
                    await c.send(f"Pairing completed.")
                else: 
                    await c.send("Failed to complete pairing. Make sure the users are paired and active.")
            else:
                await c.send("Unknown command. Use !dd init, !dd generate, or !dd complete <user1> <user2>.")


if __name__ == "__main__":
    bot = SignalBot({
        "signal_service": os.environ["SIGNAL_SERVICE"],
        "phone_number": os.environ["PHONE_NUMBER"]
    })


    db_service = DBService()

    bot.register(CFLCommands(db_service), contacts=False, groups=['bot testing']) 
    bot.start()