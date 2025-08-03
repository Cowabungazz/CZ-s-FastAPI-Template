"""
Run this module to start the application.
"""

from __future__ import annotations

import logging
from typing import Optional, Dict

from fastapi import FastAPI, Depends, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

# Routers (adjust the import path to your project layout)
from src.main.routers.monitor import monitor_router
from src.main.routers.router1 import router1_router

# Settings (Pydantic v2)
from src.main.config import get_settings


logger = logging.getLogger("uvicorn.error")
settings = get_settings()  # single, cached instance


# --------------------------
# Optional request dependency
# --------------------------
def required_headers(
    header_1: Optional[str] = Header(default=None, description="Example header 1"),
    header_2: Optional[str] = Header(default=None, description="Example header 2"),
) -> Dict[str, Optional[str]]:
    """
    Require/validate inbound headers for all endpoints (if added in `dependencies`).
    Customize validation logic as needed.
    """
    # Example: make both headers mandatory in production only
    if settings.app_env == "production":
        missing = [name for name, val in {"header_1": header_1, "header_2": header_2}.items() if not val]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required header(s): {', '.join(missing)}",
            )
    return {"header_1": header_1, "header_2": header_2}


# ---------------
# App description
# ---------------
description = f"""
---
<details>
<summary><b>Environment</b></summary>

* app_env: <code>{settings.app_env}</code><br/>
* version: <code>{getattr(settings, 'app_version', '1.0.0')}</code>
</details>
"""


# ---------------
# App factory
# ---------------
def create_app() -> FastAPI:
    app = FastAPI(
        title="WebTemplate",
        version=str(getattr(settings, "app_version", "1.0.0")),
        description=description,
        docs_url="/docs",
        redoc_url=None,
        dependencies=[Depends(required_headers)],  # enforce headers for all routes
    )

    # CORS (adjust origins)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(monitor_router, tags=["monitor"])
    app.include_router(router1_router, prefix="/router1", tags=["router1"])

    @app.on_event("startup")
    async def _on_startup():
        logger.info("[Startup] ENV=%s VERSION=%s", settings.app_env, getattr(settings, "app_version", "n/a"))

    @app.on_event("shutdown")
    async def _on_shutdown():
        logger.info("[Shutdown] Bye.")

    return app


app = create_app()


# ---------------
# CLI entrypoint
# ---------------
if __name__ == "__main__":
    import uvicorn

    # Derive runtime flags
    is_dev = settings.app_env.lower() == "development"
    host = getattr(settings, "host", "0.0.0.0")
    port = int(getattr(settings, "port", 8000))
    workers = int(getattr(settings, "workers", 2))
    log_level = str(getattr(settings, "log_level", "info")).lower()

    print("[AP Configuration]:")
    print(settings.model_dump_json(indent=2))  # pretty-print settings (no secrets ideally)

    uvicorn.run(
        app="src.main.main:app",  # adjust if your module path differs
        host=host,
        port=port,
        workers=(workers if not is_dev else 1),  # reload + multiple workers don't mix
        reload=is_dev,
        log_level=log_level,
    )
