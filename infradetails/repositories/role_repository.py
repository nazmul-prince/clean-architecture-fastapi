from abc import abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.schema.user_schema import RoleSchema
from infradetails.model.role_model import RoleModel


class RoleRepository:

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
