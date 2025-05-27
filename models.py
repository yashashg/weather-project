from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class WeatherQuery(Base):
    __tablename__ = 'weather_queries'

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String)
    location = Column(String)
    date_queried = Column(DateTime, default=datetime.utcnow)
    response = Column(String)
