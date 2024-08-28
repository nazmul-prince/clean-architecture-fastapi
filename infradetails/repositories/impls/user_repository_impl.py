from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.schema.user_schema import UserSchema, RoleSchema, UserRoleSchema
from infradetails.model.role_model import RoleModel
from infradetails.model.user_model import UserModel
from infradetails.model.user_role_model import UserRoleModel
from infradetails.repositories.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):

    async def create(self, user_schema: UserSchema, db_session: AsyncSession) -> None:
        user_model = UserModel(**user_schema.model_dump(exclude_none=True))
        db_session.add(user_model)
        await db_session.commit()

    async def get(self, db_session: AsyncSession) -> List[Optional[UserSchema]]:
        query = select(UserModel)
        result = await db_session.execute(query)
        users = result.scalars.all()
        return [UserSchema.model_validate(user) for user in users]

    async def activate_deactivate(self, user_id: int, activate: bool, db_session: AsyncSession) -> None:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values({UserModel.is_active: activate})
            .execution_options(synchronize_session="fetch")
        )
        await db_session.execute(stmt)
        await db_session.commit()

    async def get_roles_by_user_id(self, user_id: int, db_session: AsyncSession) -> List[str]:
        result = await db_session.execute(
            select(RoleModel.name)
            .join(UserRoleModel, RoleModel.id == UserRoleModel.role_id)
            .filter(UserRoleModel.user_id == user_id)
        )
        roles = result.scalars().all()
        return list(roles)

    async def get_user_by_username(self, username: str, db_session: AsyncSession) -> Optional[UserSchema]:
        result = await db_session.execute(select(UserModel).where(UserModel.username == username))
        user = result.scalars().first()
        return user

    async def assign_role_to_user(self, user_role_schema: UserRoleSchema, db_session: AsyncSession) -> None:
        # Check if role exists
        query = await db_session.execute(select(RoleModel).filter(RoleModel.id == user_role_schema.role_id))
        role = query.scalars().first()
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

        # Assign role to user
        user_role = UserRoleModel(**user_role_schema.model_dump(exclude_none=False))
        db_session.add(user_role)
        await db_session.commit()

    async def remove_role_from_user(self, user_id: int, role_id: int, db_session: AsyncSession) -> None:
        # Find the user role mapping
        query = await db_session.execute(
            select(UserRoleModel).filter(UserRoleModel.user_id == user_id, UserRoleModel.role_id == role_id)
        )
        user_role = query.scalars().first()
        if not user_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User role mapping not found")

        # Remove role from user
        await db_session.delete(user_role)
        await db_session.commit()