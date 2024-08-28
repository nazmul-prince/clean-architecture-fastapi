from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schema.user_schema import UserSchema, UserRoleSchema, RoleSchema
from app.core.usecases.user_usecase import UserUseCase
from infradetails.model.user_model import UserModel
from infradetails.repositories.user_repository import UserRepository
from app.core.utils.password_utils import get_password_hash

class UserUseCaseImpl(UserUseCase):

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_schema: UserSchema, db_session: AsyncSession) -> None:
        user_schema.password = get_password_hash(user_schema.password)
        await self.user_repository.create(user_schema, db_session)

    async def get_users(self, db_session: AsyncSession) -> List[Optional[UserSchema]]:
        users = await self.user_repository.get(db_session)
        return [UserSchema.from_orm(user) for user in users]

    async def activate_deactivate_user(self, user_id: int, activate: bool, db_session: AsyncSession) -> None:
        await self.user_repository.activate_deactivate(user_id, activate, db_session)

    async def assign_role_to_user(self, user_role_schema: UserRoleSchema, db_session: AsyncSession) -> None:
        await self.user_repository.assign_role_to_user(user_role_schema, db_session)

    async def remove_role_from_user(self, user_id: int, role_id: int, db_session: AsyncSession) -> None:
        await self.user_repository.remove_role_from_user(user_id, role_id, db_session)