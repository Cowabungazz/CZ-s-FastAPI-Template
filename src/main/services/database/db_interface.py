"""
Concrete data retriever with specific queries.
Prefer parameterized SQL over string interpolation to avoid injection.
"""

from __future__ import annotations
from typing import Any, Iterable, Optional
from .conn_factory import WrapMakeConnection


class DB_Interface(WrapMakeConnection):
    def __init__(self, dsn: str, user: str, password: str, **kwargs: Any) -> None:
        super().__init__(dsn=dsn, user=user, password=password, **kwargs)

    def insertdb(self, value1: str, dt_str: str) -> int:
        """
        Example INSERT. Use parameter placeholders compatible with your driver.
        For cx_Oracle/oracledb it's usually named binds like :1, :2, etc.
        """
        sql = """
            INSERT INTO DBNAME (column1name, column2name)
            VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD HH24:MI:SS'))
        """.strip()
        params: Iterable[Optional[str]] = (value1, dt_str)
        return self.conn.non_query(sql, params)

    def finddb1(self, value: str) -> list[dict[str, Any]]:
        """
        Example SELECT returning a list of rows.
        """
        sql = """
            SELECT *
            FROM DBNAME
            WHERE columnname = :1
        """.strip()
        params: Iterable[Optional[str]] = (value,)
        return self.conn.query(sql, params)

    def finddb2(self, value: str) -> bool:
        """
        Return True/False based on existence or a condition.
        """
        sql = """
            SELECT 1
            FROM DBNAME
            WHERE columnname = :1
            FETCH FIRST 1 ROWS ONLY
        """.strip()
        rows = self.conn.query(sql, (value,))
        return len(rows) > 0
