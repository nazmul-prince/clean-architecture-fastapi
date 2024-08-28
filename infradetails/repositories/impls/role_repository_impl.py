from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.schema.user_schema import RoleSchema
from infradetails.model.role_model import RoleModel
from infradetails.repositories.role_repository import RoleRepository


class RoleRepositoryImpl(RoleRepository):
    async def create_role(self, role_schema: RoleSchema, db_session: AsyncSession) -> None:
        new_role = RoleModel(name=role_schema.name)
        db_session.add(new_role)
        await db_session.commit()
        await db_session.refresh(new_role)

    async def get_role(self, role_id: int, db_session: AsyncSession) -> RoleSchema:
        query = await db_session.execute(select(RoleModel).filter(RoleModel.id == role_id))
        role = query.scalars().first()
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        return RoleSchema.from_orm(role)

    async def get_all_roles(self, db_session: AsyncSession) -> List[RoleSchema]:
        query = await db_session.execute(select(RoleModel))
        roles = query.scalars().all()
        return [RoleSchema.from_orm(role) for role in roles]

    async def update_role(self, role_id: int, role_schema: RoleSchema, db_session: AsyncSession) -> RoleSchema:
        query = await db_session.execute(select(RoleModel).filter(RoleModel.id == role_id))
        role = query.scalars().first()
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

        role.name = role_schema.name
        await db_session.commit()
        await db_session.refresh(role)
        return RoleSchema.from_orm(role)

    async def delete_role(self, role_id: int, db_session: AsyncSession) -> None:
        query = await db_session.execute(select(RoleModel).filter(RoleModel.id == role_id))
        role = query.scalars().first()
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

        await db_session.delete(role)
        await db_session.commit()
