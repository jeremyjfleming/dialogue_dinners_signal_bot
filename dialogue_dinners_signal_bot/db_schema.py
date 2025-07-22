from typing import List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Column, Integer, ForeignKey

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(32))
    phone_number: Mapped[str]

    active_pairing = relationship('User', 
                            secondary='pairings',
                            primaryjoin='User.id == Pairing.member1_id && Pairing.is_active == TRUE',
                            secondaryjoin='User.id == Pairing.member2_id && Pairing.is_active == TRUE',
                            backref='paired_with')

    old_pairings = relationship('User', 
                            secondary='pairings',
                            primaryjoin='User.id == Pairing.member1_id && Pairing.is_active == FALSE',
                            secondaryjoin='User.id == Pairing.member2_id && Pairing.is_active == FALSE',
                            backref='previously_paired_with')

class Pairing(Base):
    __tablename__ = 'pairings'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    member1_id = Column(Integer, ForeignKey('users.id'))
    member2_id = Column(Integer, ForeignKey('users.id'))
    is_active: Mapped[bool] = mapped_column(default=True)

