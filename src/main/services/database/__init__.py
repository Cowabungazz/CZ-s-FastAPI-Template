"""
Initialize a shared DB_Interface instance configured from app settings.
"""

from __future__ import annotations
from main.services.database.db_interface import DB_Interface

# Prefer a central settings provider (pydantic v2)
try:
    from src.main.config import get_settings

    _settings = get_settings()
    # Map settings to DB connection parameters. Adjust to your config names.
    _dsn = getattr(_settings, "database_dsn", "db-host:1521/ORCLCDB")
    _user = getattr(_settings, "database_user", "user")
    _password = getattr(_settings, "database_password", "password")
    # Extra options (pool size, timeouts, etc.)
    _kwargs = dict()
except Exception:
    # Fallback placeholders if settings aren’t ready at import time
    _dsn, _user, _password, _kwargs = "db-host:1521/ORCLCDB", "user", "password", {}

db_api = DB_Interface(dsn=_dsn, user=_user, password=_password, **_kwargs)

__all__ = ["db_api", "DB_Interface"]
