"""
Health checks for the service and (optionally) dependencies.
"""

from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

def healthy_check() -> None:
    """
    Raise an exception if the service (or critical dependencies) are unhealthy.
    Keep it fast and side-effect free. Plug in quick checks if needed:
    - config presence
    - lightweight DB/Cache ping (optional)
    """
    # Example no-op check; replace with real checks if desired.
    logger.debug("Health check OK.")
    return None
