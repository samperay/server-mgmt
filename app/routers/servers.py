from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database

router = APIRouter()


# @router.post("/", response_model=schemas.Server)
# def create_server(server: schemas.ServerCreate, db: Session = Depends(database.get_db)):
#     db_server = models.Server(**server.dict())
#     db.add(db_server)
#     db.commit()
#     db.refresh(db_server)
#     return db_server


# @router.get("/", response_model=List[schemas.Server])
# def read_servers(
#     skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)
# ):
#     servers = db.query(models.Server).offset(skip).limit(limit).all()
#     return servers


# @router.get("/{identifier}", response_model=schemas.Server)
# def read_server(identifier: str, db: Session = Depends(database.get_db)):
#     server = (
#         db.query(models.Server)
#         .filter(
#             (models.Server.hostname == identifier)
#             | (models.Server.ip_address == identifier)
#         )
#         .first()
#     )
#     if server is None:
#         raise HTTPException(status_code=404, detail="Server not found")
#     return server


# @router.put("/{identifier}", response_model=schemas.Server)
# def update_server(
#     identifier: str,
#     server: schemas.ServerCreate,
#     db: Session = Depends(database.get_db),
# ):
#     db_server = (
#         db.query(models.Server)
#         .filter(
#             (models.Server.hostname == identifier)
#             | (models.Server.ip_address == identifier)
#         )
#         .first()
#     )
#     if db_server is None:
#         raise HTTPException(status_code=404, detail="Server not found")
#     for key, value in server.dict().items():
#         setattr(db_server, key, value)
#     db.commit()
#     db.refresh(db_server)
#     return db_server


# @router.delete("/{identifier}", response_model=schemas.Server)
# def delete_server(identifier: str, db: Session = Depends(database.get_db)):
#     db_server = (
#         db.query(models.Server)
#         .filter(
#             (models.Server.hostname == identifier)
#             | (models.Server.ip_address == identifier)
#         )
#         .first()
#     )
#     if db_server is None:
#         raise HTTPException(status_code=404, detail="Server not found")
#     db.delete(db_server)
#     db.commit()
#     return db_server
