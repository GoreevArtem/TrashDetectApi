from fastapi import APIRouter

from . import auth, user, request, expert

router = APIRouter()
router.include_router(auth.router)
router.include_router(user.router)
router.include_router(request.router)
router.include_router(expert.router)
