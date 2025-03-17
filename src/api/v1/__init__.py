from fastapi import APIRouter

from api.v1 import auth, route

router = APIRouter(prefix="/api/v1")

router.include_router(route.prot_router)
router.include_router(route.pub_router)
router.include_router(auth.router)


