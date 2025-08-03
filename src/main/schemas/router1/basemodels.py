"""
Router1-specific request/base models — Pydantic v2.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class sub_basemodel1(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    attribute1: str = Field(..., examples=["value1"])
    attribute2: str = Field(..., examples=["value2"])
    attribute3: str = Field(..., examples=["value3"])
    attribute4: str = Field(..., examples=["value4"])
    attribute5: List[str] = Field(default_factory=list, examples=[["a", "b", "c"]])


class sub_basemodel2(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    attribute1: Optional[str] = Field(None, examples=["optional-value"])
    attribute2: Optional[List[str]] = Field(None, examples=[["x", "y"]])


class router1_basemodel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    attribute1: str = Field(..., examples=["top-level-value"])
    attribute2: sub_basemodel1
    attribute3: Optional[sub_basemodel2] = None
