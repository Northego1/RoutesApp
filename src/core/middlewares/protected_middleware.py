from typing import Awaitable, Callable, Protocol

from dependency_injector.wiring import Provide, inject
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from apps.auth.application.dto import UserDto
from apps.auth.presentation.schemas.responses import GetMeResponse
from container import Container
from core.config import ApiAccessType
from core.schema import ApiResponse, Status


class GetmeControllerProtocol(Protocol):
    async def get_me(self, request: Request, api_response: bool = True,
    ) -> GetMeResponse: ...


@inject
async def state_user(
    request: Request,
    getme_controller: GetmeControllerProtocol = Provide[Container.presentation.get_me],
) -> GetMeResponse:
    return await getme_controller.get_me(request, api_response=False)



class ProtectedMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self,
            request: Request,
            call_next: Callable[[Request],
            Awaitable[Response]],
    ) -> Response:
        if request.url.path.startswith(f"/api/v1{ApiAccessType.PROTECTED.value}"):
            try:
                user = await state_user(request=request)
                request.state.user = user
            except HTTPException as e:
                return JSONResponse(
                    status_code=401,
                    content=ApiResponse(
                        status=Status.FAILURE,
                        detail=e.detail,
                    ).model_dump(),
                )
        return await call_next(request)
