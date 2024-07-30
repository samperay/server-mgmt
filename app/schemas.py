from pydantic import BaseModel
from datetime import datetime


class ServerBase(BaseModel):
    name: str
    hostname: str
    ip_address: str
    location: str
    status: str
    os: str
    cpu_cores: int
    memory_gb: float
    storage_gb: float


class ServerCreate(ServerBase):
    pass


class Server(ServerBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True
