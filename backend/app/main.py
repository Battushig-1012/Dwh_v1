import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import api_router
from .config import settings

log = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if settings.demo_mode:
        log.warning("DEMO_MODE=true — in-memory MVP data (PostgreSQL not required)")
    else:
        try:
            from sqlalchemy.exc import SQLAlchemyError

            from .auth.security import ensure_demo_passwords
            from .db import SessionLocal

            assert SessionLocal is not None
            db = SessionLocal()
            ensure_demo_passwords(db)
            db.close()
            log.info("Connected to PostgreSQL DWH")
        except Exception as exc:  # noqa: BLE001
            log.warning("DB startup issue: %s", exc)
    yield


app = FastAPI(
    title="BBSB Enterprise Data & Regulatory Reporting Platform",
    description="SREP / BCBS 239 / DAMA-DMBOK — DEMO_MODE works without PostgreSQL",
    version="1.0.0-demo",
    lifespan=lifespan,
)

origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "bbsb-dwh-api", "demo_mode": settings.demo_mode}
