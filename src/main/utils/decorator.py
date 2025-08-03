"""
Exception-handling decorators for FastAPI endpoints.

Usage:
    @router.get("/x")
    @handle_except
    def endpoint(...): ...

    @router.get("/y")
    @async_handle_except
    async def endpoint_async(...): ...
"""

from __future__ import annotations

from functools import wraps
import sys
import traceback
import logging
from typing import Any, Callable, TypeVar, Awaitable, cast

from fastapi import status

# Adjust the import path to match your layout
from src.main.schemas import ResultStatusEm, InternalServerErrorModel
from src.main.utils.resp_util import handle_resp

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])
AF = TypeVar("AF", bound=Callable[..., Awaitable[Any]])


def _format_exc(e: Exception) -> str:
    """
    Build a concise error message with file/line/function and exception detail.
    """
    error_class = e.__class__.__name__
    detail = e.args[0] if e.args else ""
    _, _, tb = sys.exc_info()
    if tb is None:
        return f"[{error_class}] {detail}"

    last = traceback.extract_tb(tb)[-1]
    file_name, line_num, func_name = last.filename, last.lineno, last.name
    return f'File "{file_name}", line {line_num}, in {func_name}: [{error_class}] {detail}'


def handle_except(func: F) -> F:
    """
    Sync exception wrapper: returns standardized error response on failure.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Log full traceback for observability; return concise message to client.
            logger.exception("Unhandled exception in %s", func.__name__)
            err_msg = _format_exc(e)
            model = InternalServerErrorModel(
                status_code=ResultStatusEm.ng,
                msg=err_msg,
            )
            return handle_resp(model, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return cast(F, wrapper)


def async_handle_except(func: AF) -> AF:
    """
    Async exception wrapper: returns standardized error response on failure.
    """
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.exception("Unhandled exception in %s", func.__name__)
            err_msg = _format_exc(e)
            model = InternalServerErrorModel(
                status_code=ResultStatusEm.ng,
                msg=err_msg,
            )
            return handle_resp(model, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return cast(AF, wrapper)
