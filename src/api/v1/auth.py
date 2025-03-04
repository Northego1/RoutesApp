import uuid

from fastapi import APIRouter

from apps.auth import presentation
from apps.auth.presentation.schemas import responses as resp
from core.schema import ApiResponse as ApiResp

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        404: {"model": ApiResp[None, resp.UserNotFoundResponse]},
    },
)


@router.post(
        "/registration",
        status_code=201,
        responses={404: {"model": None}},
)
async def register(
        controller: presentation.register_controller,
) -> ApiResp[resp.RegisterResponse, None]:
    return await controller.register()


@router.post("/login", status_code=200)
async def login(
        controller: presentation.login_controller,
) -> ApiResp[resp.LoginResponse, None]:
    return await controller.login()


@router.post("/refresh", status_code=200)
async def refresh_jwt(
        controller: presentation.refresh_controller,
) -> ApiResp[resp.RefreshAccessJwtResponse, None]:
    return await controller.refresh()


@router.get("/user/{user_id}", status_code=200)
async def get_user(
        user_id: uuid.UUID,
        controller: presentation.get_user_controller,
) -> ApiResp[resp.GetUserResponse, None]:
    return await controller.get_user(user_id)


@router.post("/logout", status_code=204)
async def logout(controller: presentation.logout_controller) -> None:
    return await controller.logout()


@router.patch("/update", status_code=204)
async def update_user(controller: presentation.update_controller) -> None:
    return await controller.update_user()
