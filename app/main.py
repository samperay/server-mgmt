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
from datetime import datetime


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


@app.get("/create", response_class=HTMLResponse)
def create_server(request: Request):
    return templates.TemplateResponse(
        "create.html", {"request": request, "title": "Create Server"}
    )


@app.post("/servers", response_class=RedirectResponse)
def add_server(
    name=Form(...),
    hostname=Form(...),
    ip_address=Form(...),
    location=Form(...),
    status=Form(...),
    os=Form(...),
    cpu_cores=Form(...),
    memory_gb=Form(...),
    storage_gb=Form(...),
    db: Session = Depends(database.get_db),
):

    server = models.Server(
        name=name,
        hostname=hostname,
        ip_address=ip_address,
        location=location,
        status=status,
        os=os,
        cpu_cores=cpu_cores,
        memory_gb=memory_gb,
        storage_gb=storage_gb,
    )

    db.add(server)
    db.commit()

    return RedirectResponse(url="/servers", status_code=302)


@app.get("/edit", response_class=HTMLResponse)
def edit_server(request: Request, name: str, db: Session = Depends(database.get_db)):
    server = db.query(models.Server).filter((models.Server.hostname == name)).first()
    if server is not None:
        server = server.__dict__
        server.pop("_sa_instance_state")

        response = templates.TemplateResponse(
            "edit.html",
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


@app.post("/servers/update", response_class=RedirectResponse)
def update_server(
    id: int = Form(...),
    name: str = Form(...),
    hostname: str = Form(...),
    ip_address: str = Form(...),
    location: str = Form(...),
    status: str = Form(...),
    os: str = Form(...),
    cpu_cores: int = Form(...),
    memory_gb: int = Form(...),
    storage_gb: int = Form(...),
    last_updated: str = Form(...),
    db: Session = Depends(database.get_db),
):
    server = db.query(models.Server).filter(models.Server.id == id).first()

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    server.name = name
    server.hostname = hostname
    server.ip_address = ip_address
    server.location = location
    server.status = status
    server.os = os
    server.cpu_cores = cpu_cores
    server.memory_gb = memory_gb
    server.storage_gb = storage_gb
    server.last_updated = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S.%f")

    db.commit()

    return RedirectResponse(url="/servers", status_code=302)


@app.get("/delete", response_class=HTMLResponse)
def delete_server(name: str, request: Request, db: Session = Depends(database.get_db)):
    server = db.query(models.Server).filter((models.Server.hostname == name)).first()

    if server is not None:
        server = server.__dict__
        server.pop("_sa_instance_state")

        response = templates.TemplateResponse(
            "delete.html",
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


@app.post("/servers/delete", response_class=RedirectResponse)
def confirm_delete_server(id: int = Form(...), db: Session = Depends(database.get_db)):
    server = db.query(models.Server).filter(models.Server.id == id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    db.delete(server)
    db.commit()

    return RedirectResponse(url="/servers", status_code=302)
