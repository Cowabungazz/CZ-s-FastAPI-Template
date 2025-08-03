"""
Initialize routers to be used across the application.
Expose `get_routers()` for the application to include them.
"""

from fastapi_utils.inferring_router import InferringRouter
from src.main.schemas import InternalServerErrorModel, SuccessResponseModel

# Common responses map you can reuse for all routers
RESPONSES_MODEL = {
    200: {"model": SuccessResponseModel, "description": "OK"},
    500: {"model": InternalServerErrorModel, "description": "Internal Server Error"},
}

# Declare routers here; import submodules to ensure routes are registered
monitor_router = InferringRouter(responses=RESPONSES_MODEL, tags=["monitor"])
router1_router = InferringRouter(responses=RESPONSES_MODEL, tags=["router1"])

# Import modules that attach routes to the above routers.
# Keep these at the bottom to avoid circular imports.
from . import monitor  # noqa: E402,F401
from . import router1  # noqa: E402,F401

def get_routers():
    """
    Return the list/tuple of routers for main app to include.
    Example:
        for r in get_routers():
            app.include_router(r)
    """
    return (monitor_router, router1_router)

__all__ = ["monitor_router", "router1_router", "get_routers"]
