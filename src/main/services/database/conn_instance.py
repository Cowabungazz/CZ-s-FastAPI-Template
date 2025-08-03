"""
DB connection instance (placeholder).
Wrap your driver or pool here. Add context management to auto-close.
"""

from __future__ import annotations
import logging
from typing import Any, Iterable, Optional

logger = logging.getLogger(__name__)


class MakeConnection:
    """
    Example thin wrapper over a DB connection/pool.
    Replace placeholders with your actual Oracle client (cx_Oracle/oracledb/etc.).
    """

    def __init__(self, dsn: str, user: str, password: str, **kwargs: Any) -> None:
        self.dsn = dsn
        self.user = user
        self.password = password
        self.kwargs = kwargs
        # self.pool = create_pool(dsn=dsn, user=user, password=password, **kwargs)
        logger.debug("MakeConnection created for DSN=%s user=%s", dsn, user)

    # --- helpers ---

    def _acquire(self):
        """
        Acquire a connection from pool/driver.
        """
        # return self.pool.acquire()
        return object()  # placeholder

    def _release(self, conn) -> None:
        """
        Release the connection.
        """
        # self.pool.release(conn)
        return None

    # --- public API ---

    def query(self, sql: str, params: Optional[Iterable[Any]] = None) -> list[dict[str, Any]]:
        """
        Execute a SELECT and return rows as list of dicts.
        """
        conn = self._acquire()
        try:
            logger.debug("QUERY: %s | params=%s", sql, params)
            # with conn.cursor() as cur:
            #     cur.execute(sql, params or [])
            #     cols = [d[0] for d in cur.description]
            #     return [dict(zip(cols, row)) for row in cur.fetchall()]
            return []  # placeholder return
        finally:
            self._release(conn)

    def non_query(self, sql: str, params: Optional[Iterable[Any]] = None) -> int:
        """
        Execute INSERT/UPDATE/DELETE; return affected row count.
        """
        conn = self._acquire()
        try:
            logger.debug("NON_QUERY: %s | params=%s", sql, params)
            # with conn.cursor() as cur:
            #     cur.execute(sql, params or [])
            #     conn.commit()
            #     return cur.rowcount or 0
            return 1  # placeholder affected rows
        finally:
            self._release(conn)
