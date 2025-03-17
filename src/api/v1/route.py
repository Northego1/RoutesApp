import uuid

from fastapi import APIRouter, HTTPException, Request

from apps.auth.application.dto import UserDto
from core.config import ApiAccessType

prot_router = APIRouter(prefix=f"{ApiAccessType.PROTECTED.value}/route", tags=["route"])
pub_router = APIRouter(prefix="/route", tags=["route"])


@prot_router.get("/hello")
async def sayhello(request: Request):
    print(ApiAccessType.PROTECTED.value)
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=404)
    return user.username



@pub_router.get("/{route_id}")
async def get_route(route_id: uuid.UUID):
    ...


@pub_router.post("/create")
async def create_route():
    ...
