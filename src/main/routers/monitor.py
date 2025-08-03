"""
Health/monitoring endpoints.
"""

from fastapi_utils.cbv import cbv
from . import monitor_router

from src.main.utils.decorator import handle_except
from src.main.utils.resp_util import handle_resp
from src.main.schemas import SuccessResponseModel

from src.main.services.monitor import healthy_check as svc_healthy_check  # adjust path if needed


@cbv(monitor_router)
class MonitorAPI:
    @monitor_router.get("/healthy", summary="Health check", response_model=SuccessResponseModel)
    @handle_except
    def healthy(self):
        """
        Simple health probe endpoint.
        """
        svc_healthy_check()  # raises if unhealthy
        return handle_resp(SuccessResponseModel())
