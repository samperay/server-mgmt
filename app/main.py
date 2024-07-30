from ast import For
from asyncio import Server
import stat
from fastapi import FastAPI, Request, Depends, Form, HTTPException, status
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
def get_servers(request: Request, db: Session = Depends(database.get_db)):
    servers = db.query(models.Server).all()
    servers = [server.__dict__ for server in servers]
    for server in servers:
        server.pop("_sa_instance_state")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "servers": servers,
        },
        status_code=200,
    )


@app.post("/search", response_class=RedirectResponse)
def search_servers(name: str = Form(...)):
    return RedirectResponse("/servers/" + name, status_code=302)


@app.get("/servers/{name}", response_class=HTMLResponse)
def get_server_by_id(
    name: str, request: Request, db: Session = Depends(database.get_db)
):

    server = db.query(models.Server).filter((models.Server.hostname == name)).first()

    if server is not None:
        server = server.__dict__
        server.pop("_sa_instance_state")

        response = templates.TemplateResponse(
            "search.html",
            {
                "request": request,
                "server": server,
            },
        )
        return response
    else:
        response = templates.TemplateResponse(
            "search.html",
            {
                "request": request,
                "server": None,
            },
        )
        return response
