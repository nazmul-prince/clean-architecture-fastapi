from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schema.user_schema import RoleSchema
from app.core.usecases.role_usecase import RoleUseCase
from app.core.usecases.user_usecase import UserUseCase
from infrastructure.configuration.db_config import get_async_db
from infrastructure.configuration.security.router_interceptor import RouterInterceptor
from infrastructure.configuration.user_bean_container import UserUseCaseMainContainer

router = APIRouter(prefix="/event-management/api/v1/private", route_class=RouterInterceptor)


# Role CRUD Endpoints
@router.post("/roles", response_model=RoleSchema)
@inject
async def create_role(role: RoleSchema, db: AsyncSession = Depends(get_async_db),
                      role_usecase: RoleUseCase = Depends(Provide[UserUseCaseMainContainer.usecases.role_usecase])):
    await role_usecase.create_role(role, db)
    return role


@router.get("/roles/{role_id}", response_model=RoleSchema)
@inject
async def get_role(role_id: int, db: AsyncSession = Depends(get_async_db),
                   role_usecase: RoleUseCase = Depends(Provide[UserUseCaseMainContainer.usecases.role_usecase])):
    return await role_usecase.get_role(role_id, db)


@router.put("/roles/{role_id}", response_model=RoleSchema)
@inject
async def update_role(
        role_id: int,
        role: RoleSchema,
        db: AsyncSession = Depends(get_async_db),
        role_usecase: RoleUseCase = Depends(Provide[UserUseCaseMainContainer.usecases.role_usecase])
):
    return await role_usecase.update_role(role_id, role, db)


@router.delete("/roles/{role_id}")
@inject
async def delete_role(role_id: int, db: AsyncSession = Depends(get_async_db),
                      role_usecase: RoleUseCase = Depends(Provide[UserUseCaseMainContainer.usecases.role_usecase])):
    await role_usecase.delete_role(role_id, db)
    return {"message": "Role deleted successfully"}
