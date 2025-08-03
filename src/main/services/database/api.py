"""
Functional facade over the shared db_api.
Routers/services import from here instead of touching the instance directly.
"""

from __future__ import annotations
from typing import Any
from . import db_api


def insertdb(value1: str, dt_str: str) -> int:
    """
    Insert a row and return affected row count.
    """
    return db_api.insertdb(value1=value1, dt_str=dt_str)


def finddb1(value: str) -> list[dict[str, Any]]:
    """
    Return rows for the given value.
    """
    return db_api.finddb1(value=value)


def finddb2(value: str) -> bool:
    """
    Return True if a row exists for the given value.
    """
    return db_api.finddb2(value=value)
