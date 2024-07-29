# create_dummy_data.py
from sqlalchemy.orm import Session
from app import models, database


def create_dummy_data(db: Session):
    dummy_servers = [
        {
            "name": "Server 1",
            "hostname": "server1.local",
            "ip_address": "192.168.1.1",
            "location": "Data Center A",
            "status": "active",
            "os": "Ubuntu 20.04",
            "cpu_cores": 4,
            "memory_gb": 16.0,
            "storage_gb": 256.0,
        },
        {
            "name": "Server 2",
            "hostname": "server2.local",
            "ip_address": "192.168.1.2",
            "location": "Data Center B",
            "status": "maintenance",
            "os": "CentOS 7",
            "cpu_cores": 8,
            "memory_gb": 32.0,
            "storage_gb": 512.0,
        },
        {
            "name": "Server 3",
            "hostname": "server3.local",
            "ip_address": "192.168.1.3",
            "location": "Data Center A",
            "status": "active",
            "os": "Windows Server 2019",
            "cpu_cores": 16,
            "memory_gb": 64.0,
            "storage_gb": 1024.0,
        },
    ]

    for server_data in dummy_servers:
        server = models.Server(**server_data)
        db.add(server)
    db.commit()


if __name__ == "__main__":
    db = database.SessionLocal()
    create_dummy_data(db)
    db.close()
