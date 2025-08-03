"""
Router1 service logic.
Expose a simple function `service_a(...)` and a class for more complex use.
"""

from __future__ import annotations
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class ServiceA:
    def __init__(self, param1: str, param2: Optional[str] = None) -> None:
        self.param1 = param1
        self.param2 = param2

    def function1(self) -> dict[str, Any]:
        """
        Example operation. Replace with your business logic.
        """
        logger.info("ServiceA.function1 called")
        try:
            # ... do something that can fail
            result = {"status": "ok", "param1": self.param1, "param2": self.param2}
            logger.debug("function1 result: %s", result)
            return result
        except ValueError as e: #A general python exception
            # Handle specific exceptions first
            # Log the error and re-raise as a more specific error if needed
            logger.exception("Specific failure in function1: %s", e)
            raise ValueError("specific try error") from e
        except Exception as e:  # keep broad except at the end
            logger.exception("Unexpected failure in function1: %s", e)
            raise RuntimeError("unexpected error in ServiceA.function1") from e

    def function2(self) -> None:
        """
        Another example operation.
        """
        logger.info("ServiceA.function2 called")
        # ... do work
        return None


# Convenience function so routers can call `service_a(username)` directly.
def service_a(param1: str, param2: Optional[str] = None) -> dict[str, Any]:
    svc = ServiceA(param1=param1, param2=param2)
    return svc.function1()
