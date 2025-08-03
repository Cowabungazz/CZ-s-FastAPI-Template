"""
Router1-specific response models — Pydantic v2.
"""

from __future__ import annotations

from typing import Any, List

from pydantic import Field

from src.main.schemas.base import BaseResponseModel


class Router1ResponseModel(BaseResponseModel):
    data: List[Any] = Field(
        default_factory=list,
        description="List payload for Router1 responses.",
        examples=[[{"id": 1, "name": "foo"}]],
    )
