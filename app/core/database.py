import pkgutil
import importlib
import logging
from sqlalchemy import create_engine, Column, Integer, DateTime, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declared_attr
from sqlalchemy.sql import func

from app.core.config import settings

logger = logging.getLogger(__name__)

db_status_info = {
    "connected": False,
    "engine": "Unknown",
    "url": settings.DATABASE_URL,
    "fallback_active": False,
    "error": None
}

is_sqlite = settings.DATABASE_URL.startswith("sqlite")
if is_sqlite:
    connect_args = {"check_same_thread": False}
    engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_recycle=1800,
        connect_args={"connect_timeout": 10},
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """ORM base with standard id and audit columns."""

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _import_all_models():
    import app.models as models_pkg
    for _, name, _ in pkgutil.iter_modules(models_pkg.__path__):
        importlib.import_module(f"app.models.{name}")


def init_db():
    """
    Verify database connectivity on startup.
    Schema is managed by Alembic migrations (run via run_dev.ps1 or deploy).
    """
    global engine, SessionLocal

    primary_url = settings.DATABASE_URL
    is_primary_sqlite = primary_url.startswith("sqlite")

    db_status_info["engine"] = "SQLite" if is_primary_sqlite else "PostgreSQL"
    db_status_info["url"] = primary_url

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        db_status_info["connected"] = True
        db_status_info["fallback_active"] = False
        db_status_info["error"] = None
        logger.info("Successfully connected to primary database: %s", db_status_info["engine"])

    except Exception as e:
        logger.error("Failed to connect to primary database at %s: %s", primary_url, e)

        if not is_primary_sqlite and settings.ALLOW_SQLITE_FALLBACK:
            import os
            fallback_url = settings.FALLBACK_DATABASE_URL
            logger.warning(
                "ALLOW_SQLITE_FALLBACK is True. Re-binding to SQLite at %s",
                fallback_url,
            )
            connect_args = {"check_same_thread": False}
            engine = create_engine(fallback_url, connect_args=connect_args)
            SessionLocal.configure(bind=engine)

            db_status_info["connected"] = True
            db_status_info["engine"] = "SQLite (Fallback)"
            db_status_info["url"] = fallback_url
            db_status_info["fallback_active"] = True
            db_status_info["error"] = f"Primary DB connection failed: {str(e)}"

            db_path = fallback_url.replace("sqlite:///", "")
            if "/" in db_path or "\\" in db_path:
                os.makedirs(os.path.dirname(db_path), exist_ok=True)

            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
        else:
            db_status_info["connected"] = False
            db_status_info["error"] = str(e)
            raise

    _import_all_models()
