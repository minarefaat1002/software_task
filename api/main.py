from fastapi import FastAPI, status
from .routes.categories import category_router
from contextlib import asynccontextmanager
from .db.db import init_db
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

@asynccontextmanager
async def life_span(app:FastAPI):
    """
    Async context manager for application lifecycle events.
    
    Actions:
    - On startup: Initializes database connection
    - On shutdown: Prints termination message
    """
    print("server is starting...")
    await init_db()
    yield 
    print("server has been stopped")



version = "v1"

app = FastAPI(
    title="categories",
    description="A REST API for categories web service",
    version=version,
    lifespan=life_span
)
app.include_router(category_router, prefix=f"/api/{version}/categories", tags = ["categories"])




templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    """
    Async context manager for application lifecycle events.
    
    Actions:
    - On startup: Initializes database connection
    - On shutdown: Prints termination message
    """
    return templates.TemplateResponse("index.html", {"request": request})

