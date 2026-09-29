from pathlib import Path

from fastapi import (
    FastAPI,
    Request
)

from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates

from .database import (
    Base,
    engine
)

from .routers import (
    auth,
    recommendations,
    history,
    session
)

from .config import settings


BASE = Path(__file__).resolve().parent


# Create database tables
Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title=settings.app_name,
    version="1.0.0"
)


# Static files
app.mount(
    "/static",
    StaticFiles(
        directory=BASE / "static"
    ),
    name="static"
)


# Templates
templates = Jinja2Templates(
    directory=BASE / "templates"
)


# Routers
app.include_router(auth.router)

app.include_router(
    recommendations.router
)

app.include_router(
    history.router
)

app.include_router(
    session.router
)


@app.get(
    "/",
    response_class=HTMLResponse
)
def index(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


@app.get(
    "/login",
    response_class=HTMLResponse
)
def login_page(request: Request):

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request
        }
    )


@app.get(
    "/register",
    response_class=HTMLResponse
)
def register_page(request: Request):

    return templates.TemplateResponse(
        "register.html",
        {
            "request": request
        }
    )


@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard(request: Request):

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request
        }
    )


@app.get(
    "/planner/{planner}",
    response_class=HTMLResponse
)
def planner(
    request: Request,
    planner: str
):

    if planner not in {
        "home",
        "party",
        "jewelry"
    }:

        return HTMLResponse(
            "Not found",
            status_code=404
        )

    return templates.TemplateResponse(
        f"{planner}.html",
        {
            "request": request
        }
    )


@app.get(
    "/history",
    response_class=HTMLResponse
)
def history_page(request: Request):

    return templates.TemplateResponse(
        "history.html",
        {
            "request": request
        }
    )


@app.get("/health")
def health():

    return {
        "status": "ok",
        "app": settings.app_name
    }


@app.get("/startup")
def startup_status():

    return {
        "status": "ready",
        "database": "initialized",
        "gemini_configured": bool(
            settings.gemini_api_key
        )
    }
