from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dialogue_dinners_signal_bot.db_schema import Base, User, Pairing
import random


class DBService:
    

    def __init__(self):    
        self.engine = create_engine("sqlite:///dialogue_dinners.db", echo=True)
        Base.metadata.create_all(self.engine)

    def complete(self, user_1, user_2):
        with Session(self.engine) as session:
            # find the pairing in the database
            pair = session.query(Pairing).filter(
                Pairing.member1.has(User.uuid == user_1["uuid"]),
                Pairing.member2.has(User.uuid == user_2["uuid"]),
                Pairing.is_active == True
            ).first()
            if pair is None:  # check the reverse pairing
                pair = session.query(Pairing).filter(
                    Pairing.member1.has(User.uuid == user_2["uuid"]),
                    Pairing.member2.has(User.uuid == user_1["uuid"]),
                    Pairing.is_active == True
                ).first()
            if pair:
                pair.is_active = False
                session.commit()
                return True
            else:
                print(f"No active pairing found for {user_1} and {user_2}")
                return False
        
    def add(self, user_list):
        print(user_list[0])
        with Session(self.engine) as session:
            # add users to the database
            for user in user_list:
                user = User(phone_number=user["number"], uuid=user["uuid"])
                session.add(user)
            session.commit()    
        

    def get_pairings(self):
        with Session(self.engine) as session:
            pairings = session.query(Pairing).all()
            return [(pair.member1.uuid, pair.member2.uuid) for pair in pairings if pair.is_active]
    def generate(self):
        with Session(self.engine) as session:
            # get list of users that do not have an active pairing
            users = session.query(User).filter(User.active_pairing == None).all()
            if len(users) < 2:
                print("Not enough users to generate pairs.")
                return []

            for i in range(2**len(users)): # all combinations of pairs
                # TODO: this will cause duplicates that are checked. figure out a better way to go through all possible pairings

                random.shuffle(users)
                pairs = []
                for j in range(0, len(users), 2):
                    if j + 1 < len(users):
                        # check if pair already exists
                        if not self._isPair(users[j], users[j + 1]):
                            pairs.append((users[j], users[j + 1]))
                        else:
                            # if the pair already exists, break and try again with new shuffle
                            pairs = []
                            break
                if len(pairs) > 0:
                    # add the pairs to the database
                    for pair in pairs:
                        new_pairing = Pairing(member1=pair[0], member2=pair[1])
                        session.add(new_pairing)
                    session.commit()
                    return pairs  

    def regenerate(self):
        with Session(self.engine) as session:
            # delete all active pairings
            session.query(Pairing).filter(Pairing.is_active == True).delete()
            session.commit()
            return self.generate()


            
    def reset(self):
        # reset the database
        with Session(self.engine) as session:
            session.query(User).delete()
            session.query(Pairing).delete()
            session.commit()
    
    def _isPair(self, user_1: User, user_2: User):
        with Session(self.engine) as session:
            # check if the users are paired
            pair = session.query(Pairing).filter(
                Pairing.member1.has(User.id == user_1.id),
                Pairing.member2.has(User.id == user_2.id),
            ).first()
            if (pair is None): # check the reverse pairing
                pair = session.query(Pairing).filter(
                    Pairing.member1.has(User.id == user_2.id),
                    Pairing.member2.has(User.id == user_1.id),
                ).first()
            return pair is not None
    def _genRandomPairs(self, items):
        # Shuffle the list and create pairs
        
        return pairs

