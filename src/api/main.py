"""
main.py - Punto de entrada de la aplicacion FastAPI.
"""

from __future__ import annotations

import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

from src.api.router import router
from src.core.config import ALLOWED_HOSTS, ALLOWED_ORIGINS, API_PREFIX, APP_NAME, APP_VERSION, FRONTEND_DIR
from src.services.storage import initialize_db


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("sentiment-api")

app = FastAPI(
    title=f"{APP_NAME} API",
    description="API REST para clasificar sentimiento en textos en espanol.",
    version=APP_VERSION,
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    initialize_db()
    logger.info("Aplicacion preparada")


@app.middleware("http")
async def add_runtime_headers(request: Request, call_next):
    started_at = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - started_at
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled server error: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Error interno no controlado."})


@app.get("/", include_in_schema=False)
def frontend() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/app", include_in_schema=False)
def frontend_alias() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


app.include_router(router, prefix=API_PREFIX)
