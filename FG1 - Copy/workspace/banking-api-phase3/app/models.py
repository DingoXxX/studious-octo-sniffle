from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class License(Base):
    __tablename__ = "licenses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    license_key = Column(String, unique=True)
    expiry = Column(DateTime, default=datetime.datetime.utcnow)
