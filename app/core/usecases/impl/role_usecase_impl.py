from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.schema.user_schema import RoleSchema
from app.core.usecases.role_usecase import RoleUseCase
from infradetails.repositories.role_repository import RoleRepository


class RoleUseCaseImpl(RoleUseCase):
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    async def create_role(self, role_schema: RoleSchema, db_session: AsyncSession) -> None:
        new_role = await self.role_repository.create_role(role_schema, db_session)

    async def get_role(self, role_id: int, db_session: AsyncSession) -> RoleSchema:
        role = await self.role_repository.get_role(role_id, db_session)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        return RoleSchema.from_orm(role)

    async def get_all_roles(self, db_session: AsyncSession) -> List[RoleSchema]:
        roles = await self.role_repository.get_all_roles(db_session)
        return [RoleSchema.from_orm(role) for role in roles]

    async def update_role(self, role_id: int, role_schema: RoleSchema, db_session: AsyncSession) -> RoleSchema:
        role = await self.role_repository.get_role(role_id, db_session)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

        updated_role = await self.role_repository.update_role(role, role_schema, db_session)
        return RoleSchema.from_orm(updated_role)

    async def delete_role(self, role_id: int, db_session: AsyncSession) -> None:
        role = await self.role_repository.get_role(role_id, db_session)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

        await self.role_repository.delete_role(role, db_session)