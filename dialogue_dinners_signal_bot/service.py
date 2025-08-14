from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dialogue_dinners_signal_bot.db_schema import Base, User, Pairing
import random


class DBService:
    

    def __init__(self):    
        self.engine = create_engine("sqlite:///data/dialogue_dinners.db", echo=True)
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
                # check if user already exists
                existing_user = session.query(User).filter(User.uuid == user["uuid"]).first()
                if existing_user:
                    print(f"User {user['uuid']} already exists in the database.")
                    continue
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

            for i in range(len(users)): # all combinations of pairs

                pairs = []
                random.shuffle(users)  # shuffle the users to get random pairs
                for j in range(i + 1, len(users)):
                    if not self._isPair(users[i], users[j]):
                        pairs.append((users[i], users[j]))
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
                    return [(pairs.member1.uuid, pairs.member2.uuid) for pair in pairs]  
            return []  # no valid pairs found, return empty list
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

