from fastapi import FastAPI, Request, Depends, Form, HTTPException
from app.database import engine
from app.models import Base
from app.routers import servers
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import models, schemas, database

app = FastAPI()

# Configure Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Ensure the database and tables are created
Base.metadata.create_all(bind=engine)

# Include the routers
app.include_router(servers.router, prefix="/servers", tags=["servers"])


@app.get("/", response_class=RedirectResponse)
def read_home(request: Request):
    return RedirectResponse(url="/servers")


@app.get("/servers", response_class=HTMLResponse)
def read_servers(request: Request, db: Session = Depends(database.get_db)):
    servers = db.query(models.Server).all()
    # don't display object id but only server data
    servers = [server.__dict__ for server in servers]
    for server in servers:
        server.pop("_sa_instance_state")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "servers": servers,
            "title": "Home",
        },
        status_code=200,
    )
