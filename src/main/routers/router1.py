"""
Example business router (Router1).
"""

from fastapi_utils.cbv import cbv
from . import router1_router

from src.main.utils.resp_util import handle_resp
from src.main.utils.decorator import handle_except

from src.main.schemas.router1.responsemodels import Router1ResponseModel
from src.main.schemas.router1.basemodels import Router1BaseModel  # request model

from src.main.config import get_settings  # loads configs (from your earlier __init__.py)
from src.main.services.router1.service_a import service_a
from src.main.utils.router1.utils_a import utils_a
from main.services.database.api import insert_db  # add other db functions as needed


@cbv(router1_router)
class Router1API:
    @router1_router.post(
        "/posturl",
        summary="Process Router1 request",
        response_model=Router1ResponseModel,
    )
    @handle_except  # catches, logs, and re-raises as your standardized errors
    def router1_post(self, request: Router1BaseModel):
        """
        Example POST endpoint showing service, utils, and DB usage.
        """
        settings = get_settings()  # access configs
        # domain logic
        service_a(request.username)
        utils_a()
        insert_db(settings.componentA.compA_variable)  # example config use

        return handle_resp(Router1ResponseModel(data={"message": "success"}))
