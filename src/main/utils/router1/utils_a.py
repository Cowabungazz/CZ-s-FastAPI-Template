"""
Router1 utilities — lightweight, stateless helpers.
If you specifically want a class container, convert these to @staticmethods in a class UtilsA: to avoid needing self.
"""

from __future__ import annotations
import logging
from typing import Any

logger = logging.getLogger(__name__)


def function1(arg: str) -> str:
    """
    Example pure helper that transforms a value.
    """
    logger.debug("utils_a.function1 input=%s", arg)
    out = arg.strip().lower()
    logger.debug("utils_a.function1 output=%s", out)
    return out


def function2(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Example helper that validates/enriches a dict.
    """
    logger.debug("utils_a.function2 payload in=%s", payload)
    enriched = {**payload, "processed": True}
    logger.debug("utils_a.function2 payload out=%s", enriched)
    return enriched
