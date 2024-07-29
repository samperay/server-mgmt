from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import servers

app = FastAPI()

# Ensure the database and tables are created
Base.metadata.create_all(bind=engine)

# Include the routers
app.include_router(servers.router, prefix="/servers", tags=["servers"])
