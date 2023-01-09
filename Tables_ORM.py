from sqlalchemy import Column, Integer, Text, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Tarification(Base):
    __tablename__ = 'tarification'
    subscr_id = Column(Integer, primary_key = True)
    fee = Column(Integer)
    tariff = Column(Text)

class Subscriber(Base):
    __tablename__ = 'subscriber'
    number = Column(Text, primary_key = True)
    subscr_id = Column(Integer, ForeignKey('tarification.subscr_id'))
    name = Column(Text)
    tarification = relationship("Tarification", backref = backref('tarification'))

class Call(Base):
    __tablename__ = 'call'
    call_id = Column(Integer, primary_key = True)
    subscriber1 = Column(Text, ForeignKey('subscriber.number'))
    subscriber2 = Column(Integer, ForeignKey('subscriber.subscr_id'))
    start_time = Column(Time)
    end_time = Column(Time)
    subscr_id = relationship("Subscriber", foreign_keys = [subscriber1])
    number = relationship("Subscriber", foreign_keys = [subscriber2])