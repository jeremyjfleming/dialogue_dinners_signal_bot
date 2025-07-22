from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dialogue_dinners_signal_bot.db_schema import Base, User, Pairing



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
            print(session.query(User).filter(User.active_pairings == None).all())



            
    def reset(self):
        # reset the database
        with Session(self.engine) as session:
            session.query(User).delete()
            session.query(Pairing).delete()
            session.commit()

