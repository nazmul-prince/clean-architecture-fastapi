from fastapi import APIRouter

from infrastructure.configuration.security.router_interceptor import RouterInterceptor
from infrastructure.routes import user_controller, authentication_controller, role_controller

router = APIRouter()

# routers
router.include_router(authentication_controller.router)
router.include_router(user_controller.router)
router.include_router(role_controller.router)
