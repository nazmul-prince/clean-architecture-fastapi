from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schema.user_schema import RoleSchema


class RoleUseCase(ABC):

    @abstractmethod
    async def create_role(self, role_schema: RoleSchema, db_session: AsyncSession) -> None:
        pass

    @abstractmethod
    async def get_role(self, role_id: int, db_session: AsyncSession) -> RoleSchema:
        pass

    @abstractmethod
    async def get_all_roles(self, db_session: AsyncSession) -> List[RoleSchema]:
        pass

    @abstractmethod
    async def update_role(self, role_id: int, role_schema: RoleSchema, db_session: AsyncSession) -> RoleSchema:
        pass

    @abstractmethod
    async def delete_role(self, role_id: int, db_session: AsyncSession) -> None:
        pass
