import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from database import get_job
from sqlite3 import Connection, Row
from models import Job, Jobs

ENV = os.environ['ENVIRONMENT'] if 'ENVIRONMENT' in os.environ else None
match str(ENV).lower():
    case 'prod':
        _DEBUG = False
    case _:
        _DEBUG = True

# env vars set

app = FastAPI(debug=_DEBUG)
connection = Connection('scheduler.db')
connection.row_factory = Row



app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.auto_reload = True
templates.env.cache = {}

def to_iso_z(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")



@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):

    context = get_job(connection)
    print(context)
    # events = [
    #     {
    #         "target_iso": to_iso_z(datetime(2025,9,2,12,00,34, tzinfo=ZoneInfo("Australia/Sydney")))
    #     },
    #     {
    #         "target_iso": to_iso_z(datetime(2025,12,11,12,00,34, tzinfo=ZoneInfo("Australia/Sydney")))
    #     }
    # ]
    return templates.TemplateResponse(request, "index.html", context=context.model_dump())

# Dashboard
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard/dashboard.html", {"request": request})

# Login
@app.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login/login.html", {"request": request})

# Jobs list
@app.get("/jobs", response_class=HTMLResponse)
def jobs(request: Request):
    return templates.TemplateResponse("jobs/jobs.html", {"request": request})

# Job detail
@app.get("/jobs/{job_id}", response_class=HTMLResponse)
def job_detail(request: Request, job_id: int):
    return templates.TemplateResponse("jobs/job_detail.html", {"request": request, "job_id": job_id})

# Profile
@app.get("/profile", response_class=HTMLResponse)
def profile(request: Request):
    return templates.TemplateResponse("profile/profile.html", {"request": request})

# Admin dashboard
@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    return templates.TemplateResponse("dashboard/admin_dashboard.html", {"request": request})

# Global handler for all 4XX client errors
@app.exception_handler(StarletteHTTPException)
async def client_error_handler(request: Request, exc: StarletteHTTPException):
    if 400 <= exc.status_code < 500:
        if exc.status_code == 404:
            return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)
        elif exc.status_code == 403:
            return templates.TemplateResponse("errors/403.html", {"request": request}, status_code=403)
        return templates.TemplateResponse("errors/4xx.html", {"request": request, "status_code": exc.status_code}, status_code=exc.status_code)
    # For non-4XX errors, re-raise
    raise exc