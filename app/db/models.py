from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Apod(Base):
    __tablename__ = "apod"

    date = Column(DateTime, primary_key=True)
    title = Column(String)
    explanation = Column(String)
    image_url = Column(String)
    hd_image_url = Column(String)


class Neo(Base):
    __tablename__ = "neo"

    id = Column(String, primary_key=True)
    name = Column(String)
    event_date = Column(DateTime)
    velocity_kph = Column(Float)
    miss_distance_km = Column(Float)
    diameter_min_km = Column(Float)
    diameter_max_km = Column(Float)
    is_hazardous = Column(Boolean)


class MarsPhoto(Base):
    __tablename__ = "mars_photos"

    id = Column(Integer, primary_key=True)
    image_url = Column(String)
    earth_date = Column(DateTime)
    camera_name = Column(String)
    rover_name = Column(String)
