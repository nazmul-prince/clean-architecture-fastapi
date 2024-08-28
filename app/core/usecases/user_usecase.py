from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schema.user_schema import UserSchema, RoleSchema, UserRoleSchema


class UserUseCase(ABC):
    @abstractmethod
    async def create_user(self, user_schema: UserSchema, db_session: AsyncSession) -> None:
        pass

    @abstractmethod
    async def get_users(self, db_session: AsyncSession) -> List[Optional[UserSchema]]:
        pass

    @abstractmethod
    async def activate_deactivate_user(self, user_id: int, activate: bool, db_session: AsyncSession) -> None:
        pass

    @abstractmethod
    async def assign_role_to_user(self, user_role_schema: UserRoleSchema, db_session: AsyncSession) -> None:
        pass

    @abstractmethod
    async def remove_role_from_user(self, user_id: int, role_id: int, db_session: AsyncSession) -> None:
        pass
