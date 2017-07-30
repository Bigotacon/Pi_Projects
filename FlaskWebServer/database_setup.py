from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import datetime

Base = declarative_base()

class Measurements(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    humidity = Column(Integer)
    pressure = Column(Integer)
    temp = Column(Integer)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'created_date': self.created_date,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'temp': self.temp,
        }

class Message(Base):
    __tablename__ ='message'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    message = Column(String(250))
    #count =  Column(Integer)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.message,
            #'count': self.count,
        }

engine = create_engine('sqlite:///flaskwebserver.db')


Base.metadata.create_all(engine)
