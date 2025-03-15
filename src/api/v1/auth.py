import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, Response

from api.v1 import protocols as proto
from apps.auth.presentation.schemas import requests as req
from apps.auth.presentation.schemas import responses as resp
from container import Container
from core.schema import ApiResponse as ApiResp

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        404: {"model": ApiResp[None, resp.UserNotFoundResponse]},
        401: {"model": ApiResp[None, str | dict]},
    },
)


@router.post(
        "/registration",
        status_code=201,
        responses={404: {"model": None}},
)
@inject
async def register(
        response: Response,
        request_data: req.RegisterRequest,
        cl: proto.RegisterControllerProtocol = Depends(Provide[Container.presentation.register]),
) -> ApiResp[resp.RegisterResponse, None]:
    return await cl.register(response, request_data)


@router.post("/login", status_code=200)
@inject
async def login(
        response: Response,
        request_data: req.LoginRequest,
        cl: proto.LoginControllerProtocol = Depends(Provide[Container.presentation.login]),
) -> ApiResp[resp.LoginResponse, None]:
    return await cl.login(response, request_data)


@router.post("/refresh", status_code=200)
@inject
async def refresh_jwt(
        request: Request,
        cl: proto.RefreshJwtControllerProtocol = Depends(Provide[Container.presentation.refresh_jwt]),
) -> ApiResp[resp.RefreshAccessJwtResponse, None]:
    return await cl.refresh(request)


@router.get("/user", status_code=200)
@inject
async def get_user(
    request: Request,
    cl: proto.GetUserControllerProtocol = Depends(Provide[Container.presentation.get_me]),
) -> ApiResp[resp.GetMeResponse, None]:
    return await cl.get_me(request)


@router.post("/logout", status_code=204)
@inject
async def logout(
    cl: proto.LogoutControllerProtocol = Depends(Provide[Container.presentation.logout]),
) -> None:
    return await cl.logout()


@router.patch("/user/{user_id}/update", status_code=204)
@inject
async def update_user(
    user_id: uuid.UUID,
    request_data: req.UpdateUserRequest,
    cl: proto.UpdateControllerProtocol = Depends(Provide[Container.presentation.update]),
) -> None:
    return await cl.update_user(user_id, request_data)
