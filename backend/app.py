import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .db import init_db
from .routers import judging, sessions, targets

app = FastAPI(title="RV Monitor Agent")

# Initialize DB on startup
@app.on_event("startup")
def _startup():
    schema = os.path.join(os.path.dirname(__file__), "schema.sql")
    init_db(schema)

# Routers
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(judging.router, prefix="/judging", tags=["judging"])
app.include_router(targets.router, prefix="/targets", tags=["targets"])

# Minimal static UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/health")
def health():
    return {"ok": True}
