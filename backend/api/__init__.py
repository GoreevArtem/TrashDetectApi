from fastapi import APIRouter

from . import auth, user, request

router = APIRouter()
router.include_router(auth.router)
router.include_router(user.router)
router.include_router(request.router)
