"""
backend\app\main.py
Main FastAPI application entrypoint for WaterLevel.


✅ Responsibilities:
- Load environment variables
- Initialize database (SQLAlchemy)
- Register middlewares (CORS, config lock)
- Include routers (auth, panels, config_lock, etc.)
- Provide health and root endpoints
- Catch and log global exceptions
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from dotenv import load_dotenv
import os

# -------------------------------------------------------------------
# 1️⃣ Load environment variables
# -------------------------------------------------------------------
load_dotenv()

# -------------------------------------------------------------------
# 2️⃣ Configure logging
# -------------------------------------------------------------------
from app.logging_config import setup_logging, logger

setup_logging()

# Now you can use:
logger.info("App started")

# -------------------------------------------------------------------
# 3️⃣ Create FastAPI instance
# -------------------------------------------------------------------

app = FastAPI(
    title=os.getenv("APP_TITLE", "WaterLevel API"),
    description=os.getenv("APP_DESCRIPTION", "Backend for WaterLevel telemetry/dashboard"),
    version=os.getenv("APP_VERSION", "1.0.0"),
)

# -------------------------------------------------------------------
# 4️⃣ Database setup (optional but auto-connect if available)
# -------------------------------------------------------------------
engine = None
Base = None
get_db = None

try:
    # This should exist: backend/app/db/database.py
    from app.db.database import engine as db_engine, Base as db_Base, get_db as db_get_db
    engine = db_engine
    Base = db_Base
    get_db = db_get_db
    logger.info("✅ Database module loaded successfully.")
except Exception as e:
    logger.warning("⚠️ Could not import database. Continuing without DB.")
    logger.debug("Database import error details:", exc_info=e)

# -------------------------------------------------------------------
# 5️⃣ Startup & Shutdown Events
# -------------------------------------------------------------------
@app.on_event("startup")
def on_startup():
    logger.info("🚀 Application starting...")
    if Base and engine:
        try:
            logger.info("Creating database tables if they don't exist...")
            Base.metadata.create_all(bind=engine)
            logger.info("✅ Database tables ready.")
        except Exception as e:
            logger.exception("❌ Failed to create database tables: %s", e)
    else:
        logger.info("Skipping DB initialization (engine/Base missing).")

@app.on_event("shutdown")
def on_shutdown():
    logger.info("🛑 Application shutdown complete.")

# -------------------------------------------------------------------
# 6️⃣ CORS Middleware
# -------------------------------------------------------------------
_allow_any_origin = os.getenv("ALLOW_ALL_ORIGINS", "false").lower() in ("1", "true", "yes")
_allow_origins_env = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000")

allow_origins = ["*"] if _allow_any_origin else [o.strip() for o in _allow_origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info(f"✅ CORS configured. Allowed origins: {allow_origins}")

# -------------------------------------------------------------------
# 7️⃣ Optional middleware (ConfigLockMiddleware)
# -------------------------------------------------------------------
try:
    from app.middleware.config_lock_middleware import ConfigLockMiddleware
    app.add_middleware(ConfigLockMiddleware)
    logger.info("✅ ConfigLockMiddleware loaded.")
except Exception:
    logger.debug("ℹ️ ConfigLockMiddleware not found or failed to load. Skipping.")

# -------------------------------------------------------------------
# 8️⃣ Helper to safely include routers
# -------------------------------------------------------------------
def try_include_router(module_path: str, prefix: str | None = None, tags: list | None = None):
    """
    Import a router module safely and include it if found.
    Example: try_include_router("app.routers.auth", tags=["Auth"])
    """
    try:
        module = __import__(module_path, fromlist=["router"])
        router = getattr(module, "router", None)
        if router is None:
            logger.warning(f"⚠️ {module_path} has no 'router'. Skipped.")
            return
        app.include_router(router, prefix=prefix or "")
        logger.info(f"✅ Router included from {module_path} (prefix={prefix or ''})")
    except Exception as e:
        logger.info(f"Router import failed for {module_path}: {e}", exc_info=e)

# -------------------------------------------------------------------
# 9️⃣ Include all routers
# -------------------------------------------------------------------
try_include_router("app.routers.auth", tags=["Auth"])           # will expose `/login`
try_include_router("app.routers.panels", prefix="/panels", tags=["Panels"])
try_include_router("app.routers.config_lock", tags=["Config Logs"])
try_include_router("app.routers.audit_logs", prefix="/audit", tags=["Audit Logs"])  

# Add more routers as needed:
# try_include_router("app.routers.users", prefix="/users", tags=["Users"])

# -------------------------------------------------------------------
# 🔟 Global exception handler
# -------------------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catches any unhandled exception and returns a simple JSON error.
    """
    logger.exception(f"Unhandled error during {request.method} {request.url}: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# -------------------------------------------------------------------
# 11️⃣ Health check endpoint
# -------------------------------------------------------------------
@app.get("/health", tags=["Health"])
def health_check():
    """
    Returns app and DB health status.
    """
    db_status = "unknown"
    if engine:
        try:
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            db_status = "ok"
        except Exception as e:
            db_status = f"error: {e}"
    else:
        db_status = "not configured"

    return {"status": "ok", "database": db_status}

# -------------------------------------------------------------------
# 12️⃣ Root endpoint
# -------------------------------------------------------------------
@app.get("/", tags=["Root"])
def root():
    return {"message": "🌊 WaterLevel backend is running"}

# ------------------------------
