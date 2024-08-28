from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request, APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi_keycloak_middleware import CheckPermissions, AuthorizationResult, MatchStrategy
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schema.user_schema import UserSchema, UserRoleSchema
from app.core.usecases.impl.user_usecase_impl import UserUseCaseImpl
from app.core.usecases.user_usecase import UserUseCase
from infrastructure.configuration.api_validation_bean_container import ApiValidationContainer
from infrastructure.configuration.db_config import get_async_db
from infrastructure.configuration.security.rbac_decorator import has_roles, oauth2_scheme
from infrastructure.configuration.security.router_interceptor import RouterInterceptor
from infrastructure.configuration.user_bean_container import UserUseCaseMainContainer

router = APIRouter(
    prefix="/event-management/api/v1/private",
    # route_class=RouterInterceptor
)


@router.get("/user-info", response_model=UserSchema, tags=["User"])
async def fetch_user_info(
        # current_user: str = Depends(validate_token())
):
    return {}


@router.post("/users", response_model=UserSchema)
@inject
async def create_user(
        user: UserSchema,
        db: AsyncSession = Depends(get_async_db),
        user_usecase: UserUseCase = Depends(Provide[UserUseCaseMainContainer.usecases.user_usecase])
):
    try:
        await user_usecase.create_user(user, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user


@router.get("/users", response_model=List[UserSchema])
async def get_users(
        db: AsyncSession = Depends(get_async_db),
        user_usecase: UserUseCase = Depends(Provide[UserUseCaseMainContainer.usecases.user_usecase]),
):
    try:
        users = await user_usecase.get_users(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return users


@router.put("/users/{user_id}/activate")
# @has_roles(["admin", "user"], api_validator= ApiValidationContainer.user_activation_validator())
@inject
async def activate_user(
        user_id: int,
        request: Request,
        db: AsyncSession = Depends(get_async_db),
        user_usecase: UserUseCaseImpl = Depends(Provide[UserUseCaseMainContainer.usecases.user_usecase]),
        dependencies: AuthorizationResult = Depends(CheckPermissions("f_cp")),
):
    dependencies.authorized
    print("successfull")
    # try:
    #     scope_route = request.scope.get("route")
    #     await user_usecase.activate_deactivate_user(user_id, True, db)
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=str(e))
    # return {"message": "User activated successfully"}


@router.put("/users/{user_id}/deactivate")
async def deactivate_user(
        user_id: int,
        db: AsyncSession = Depends(get_async_db),
        user_usecase: UserUseCaseImpl = Depends(Provide[UserUseCaseMainContainer.usecases.user_usecase]),
        auth_result: AuthorizationResult = Depends(CheckPermissions(["f_cp"], match_strategy=MatchStrategy.OR)),
):
    print("successfull")
    # try:
    #     await user_usecase.activate_deactivate_user(user_id, False, db)
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=str(e))
    # return {"message": "User deactivated successfully"}


# User Role Mapping Endpoints
@router.post("/users/{user_id}/roles/{role_id}")
@inject
async def assign_role_to_user(user_id: int, role_id: int, db_session: AsyncSession = Depends(get_async_db),
                              user_usecase: UserUseCase = Depends(
                                  Provide[UserUseCaseMainContainer.usecases.user_usecase])):
    user_schema = UserRoleSchema(user_id=user_id, role_id=role_id)
    await user_usecase.assign_role_to_user(user_schema, db_session)
    return {"message": "Role assigned to user successfully"}


@router.delete("/users/{user_id}/roles/{role_id}")
@inject
async def remove_role_from_user(user_id: int, role_id: int, db_session: AsyncSession = Depends(get_async_db),
                                user_usecase: UserUseCase = Depends(
                                    Provide[UserUseCaseMainContainer.usecases.user_usecase])):
    await user_usecase.remove_role_from_user(user_id, role_id, db_session)
    return {"message": "Role removed from user successfully"}
