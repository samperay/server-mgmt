from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base
from datetime import datetime


class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    hostname = Column(String, unique=True, index=True)
    ip_address = Column(String, unique=True, index=True)
    location = Column(String)
    status = Column(String)
    os = Column(String)  # Operating System
    cpu_cores = Column(Integer)
    memory_gb = Column(Float)
    storage_gb = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)
