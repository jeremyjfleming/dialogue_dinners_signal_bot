from signalbot import Command, Context
import os

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

        await c.edit(response, None, list_pairs, edit_timestamp=c.message.timestamp)

    async def handle(self, c: Context):
    

        if c.message.text.startswith("!dd") and c.message.source_number == os.environ["PHONE_NUMBER"]:
            command = c.message.text.split(" ")[1].strip().lower()
            if command == "test":
                await c.edit("Pairings are working!", edit_timestamp=c.message.timestamp)
            elif command == "poll":
                await c.edit("If you are interested in participating in dialogue dinners this semester, please react below.", edit_timestamp=c.message.timestamp)
            elif command == "add":
                user_list = c.message.mentions
                self.db_service.add(user_list)
                await c.edit("Users added", edit_timestamp=c.message.timestamp)
            elif command == "addself":
                # Add self to the database
                user = {
                    "number": c.message.source_number,
                    "uuid": c.message.source_uuid
                }
                self.db_service.add([user])
                await c.edit("Self added to the database.", edit_timestamp=c.message.timestamp)
            elif command == "pairs":
                # List current pairings
                pairs = self.db_service.get_pairings()
                if pairs:
                    await self._list_pairs(pairs, c)
                else:
                    await c.edit("Failed to list pairs or no active pairings found.", edit_timestamp=c.message.timestamp)
            elif command == "generate":
                # Generate pairings
                pairs = self.db_service.generate()
                if pairs:
                    await self._list_pairs(pairs, c)  
                else:
                    await c.edit("Failed to generate pairs or no pairs to generate!", edit_timestamp=c.message.timestamp)
            elif command == "regenerate":
                pairs = self.db_service.regenerate()
                if pairs:
                    await self._list_pairs(pairs, c)
                else:
                    await c.edit("Failed to regenerate pairs or no pairs to regenerate!", edit_timestamp=c.message.timestamp)
            elif command == "complete":
                # Complete a pairing
                user_list = c.message.mentions 
                if self.db_service.complete(user_list[0], user_list[1]):
                    await c.edit(f"Pairing completed.", edit_timestamp=c.message.timestamp)
                else: 
                    await c.edit("Failed to complete pairing. Make sure the users are paired and active.", edit_timestamp=c.message.timestamp)
            elif command == "completewithself":
                # Complete a pairing with self
                user_list = c.message.mentions 
                if self.db_service.complete(user_list[0], {"uuid": c.message.source_uuid}):
                    await c.edit(f"Pairing completed with self.", edit_timestamp=c.message.timestamp)
                else: 
                    await c.edit("Failed to complete pairing with self. Make sure the users are paired and active.", edit_timestamp=c.message.timestamp)
            elif command == "reset":
                # Reset the database
                self.db_service.reset()
                await c.edit("Database reset.", edit_timestamp=c.message.timestamp)
            elif command == "help":
                help_message = (
                    "Available commands:\n"
                    "!dd test - Test the bot\n"
                    "!dd poll - Poll for interest in dialogue dinners\n"
                    "!dd add - Add users to the database (mention users)\n"
                    "!dd addself - Add yourself to the database\n"
                    "!dd pairs - List current pairings\n"
                    "!dd generate - Generate pairings\n"
                    "!dd regenerate - Regenerate pairings\n"
                    "!dd complete - Complete a pairing (mention two users)\n"
                    "!dd completewithself - Complete a pairing with yourself (mention one user)\n"
                    "!dd reset - Reset the database\n"
                )
                await c.edit(help_message, edit_timestamp=c.message.timestamp)
            else:
                await c.edit("Unknown command. Use !dd help for a list of commands.", edit_timestamp=c.message.timestamp)
