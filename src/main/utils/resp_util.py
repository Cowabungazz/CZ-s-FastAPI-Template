"""
Response helpers for FastAPI.
"""

from __future__ import annotations

from fastapi import status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def handle_resp(model: BaseModel, status_code: int = status.HTTP_200_OK) -> JSONResponse:
    """
    Serialize a Pydantic model to a JSONResponse with the given status code.
    """
    return JSONResponse(content=jsonable_encoder(model), status_code=status_code)
