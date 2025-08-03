"""
Base class to open a DB connection for retrievers.
"""

from __future__ import annotations
from typing import Any
from main.services.database.conn_instance import MakeConnection


class WrapMakeConnection:
    def __init__(self, dsn: str, user: str, password: str, **kwargs: Any) -> None:
        self.dsn = dsn
        self.user = user
        self.password = password
        self.kwargs = kwargs
        self.conn = self.__get_conn()

    def __get_conn(self) -> MakeConnection:
        # Adapt kwargs to your driver/pool options
        return MakeConnection(self.dsn, self.user, self.password, **self.kwargs)
