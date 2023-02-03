from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String, MetaData
#from database import Base
from dataclasses import dataclass
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class Client(Base):
    __tablename__ = "client"

    cpf = Column(String(11), primary_key = True, unique = True)
    name = Column(String)
    surname = Column(String)
    adress = Column(String)
    birth = Column(String)
    email = Column(String, unique = True)
    password = Column(String)

    def __init__(self, cpf, name, surname, address, birth, email, password):
        self.cpf = cpf
        self.name = name
        self.surname = surname
        self.address = address
        self.birth = birth
        self.email = email
        self.password = password
        

    def __repr__(self):
        return '<Cliente %r>' % (self.cpf)    
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class Airport(Base):
    __tablename__ = "airport"

    iata = Column(String(3), primary_key = True, unique = True)
    name = Column(String)
    city = Column(String)
    state = Column(String(2))

    def __init__(self, iata, name, city, state):
        self.iata = iata
        self.name = name
        self.city = city
        self.state = state

class Flight(Base):
    __tablename__ = "flight"

    id = Column(Integer, primary_key = True, unique = True, autoincrement=True)
    origin = Column(ForeignKey('airport.iata'))
    destiny = Column(ForeignKey('airport.iata'))
    company = Column(String)
    passengers = Column(Integer)
    departure = Column(String)
    arrival = Column(String)
    price = Column(Float)

    def __repr__(self):
        return '<Vôo %r>' % (self.company)


    def __init__(self, id, origin, destiny, company, passengers, departure, arrival, price):
        self.id = id
        self.origin = origin
        self.destiny = destiny
        self.company = company
        self.passengers = passengers
        self.departure = departure
        self.arrival = arrival
        self.price = price
    
    def __iter__(self):
        yield from{ 
            "id": self.id,
            "origin": self.origin,
            "destiny": self.destiny,
            "company": self.company,
            "passengers": self.passengers,
            "departure": self.departure,
            "arrival": self.arrival,
            "price": self.price
            
            }

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key = True, unique = True, autoincrement=True)
    id_session = Column(Integer, ForeignKey('clientsession.id'))
    id_flight = Column(Integer, ForeignKey('flight.id'))
    date = Column(String)
    price = Column(ForeignKey('flight.price'))

    def __init__(self, id, id_session, id_flight, date, price):
        self.id = id
        self.id_session = id_session
        self.id_flight = id_flight
        self.date = date
        self.price = price

class ClientSession(Base):
    __tablename__ = "clientsession"

    id = Column(Integer, primary_key = True, unique = True, autoincrement=True)
    email_client = Column(ForeignKey('client.email'))
    date = Column(String)
    status = Column(String)

    def __init__(self, id, id_client, date, status):
        self.id = id
        self.id_client = id_client
        self.date = date
        self.status = status


