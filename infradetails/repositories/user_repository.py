from abc import ABCMeta, abstractmethod
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schema.token_schema import TokenSchema
from app.core.schema.user_schema import UserSchema, RoleSchema, UserRoleSchema
from infradetails.model.user_model import UserModel


class UserRepository(metaclass=ABCMeta):

    @abstractmethod
    async def create(self, user_schema: UserSchema, db_session: AsyncSession) -> None:
        pass

    @abstractmethod
    async def get(self, db_session: AsyncSession) -> List[Optional[UserSchema]]:
        pass

    @abstractmethod
    async def get_roles_by_user_id(self, user_id: int, db_session: AsyncSession) -> List[str]:
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str, db_session: AsyncSession) -> Optional[UserSchema]:
        pass

    @abstractmethod
    async def activate_deactivate(self, user_id: int, activate: bool, db_session: AsyncSession) -> None:
        pass

    @abstractmethod
    async def assign_role_to_user(self, user_role_schema: UserRoleSchema, db_session: AsyncSession) -> None:
        pass

    @abstractmethod
    async def remove_role_from_user(self, user_id: int, role_id: int, db_session: AsyncSession) -> None:
        pass
