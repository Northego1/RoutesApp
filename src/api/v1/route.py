import uuid

from fastapi import APIRouter

router = APIRouter(prefix="/route", tags=["route"])


@router.get("/{route_id}")
async def get_route(route_id: uuid.UUID):
    ...


@router.post("/create")
async def create_route():
    ...