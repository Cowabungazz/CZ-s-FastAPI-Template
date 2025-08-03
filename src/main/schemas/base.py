"""
Default (shared) API response models — Pydantic v2.
- `version` resolves from central settings (if available) or APP_VERSION env var.
"""

from __future__ import annotations

import os
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, StrictStr, ConfigDict


def _resolve_version() -> str:
    """Try config settings, then APP_VERSION env var, then '1.0.0'."""
    try:
        from src.main.config import get_settings  # adjust path if needed
        version = getattr(get_settings(), "app_version", None)
        if version:
            return str(version)
    except Exception:
        pass
    return os.getenv("APP_VERSION", "1.0.0")


class ResultStatusEm(str, Enum):
    ok = "0"
    ng = "1"


class BaseResponseModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    status_code: ResultStatusEm = Field(
        default=ResultStatusEm.ok,
        description="Result status: '0' for OK, '1' for NG.",
        examples=[ResultStatusEm.ok],
    )
    version: StrictStr = Field(
        default_factory=_resolve_version,
        description="API/application version.",
        examples=["1.0.0"],
    )
    msg: StrictStr = Field(
        default="",
        description="Human-readable message for the result.",
        examples=["normal end"],
    )


class SuccessResponseModel(BaseResponseModel):
    status_code: ResultStatusEm = Field(
        default=ResultStatusEm.ok, examples=[ResultStatusEm.ok]
    )
    msg: StrictStr = Field(default="normal end", examples=["normal end"])
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional payload for successful response.",
        examples=[{"items": [1, 2, 3]}],
    )


class InternalServerErrorModel(BaseResponseModel):
    status_code: ResultStatusEm = Field(
        default=ResultStatusEm.ng, examples=[ResultStatusEm.ng]
    )
    msg: StrictStr = Field(
        default="exception msg",
        description="Error/exception message.",
        examples=["exception msg"],
    )
