from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schema.authentication_schema import TokenSchema
from app.core.usecases.auth_usecase import AuthUsecase
from app.core.usecases.token_processor_usecase import TokenProcessorUseCase
from infradetails.repositories.user_repository import UserRepository
from app.core.utils.password_utils import get_password_hash, verify_password
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthUsecaseImpl(AuthUsecase):

    def __init__(self, user_repository: UserRepository, token_processor: TokenProcessorUseCase):
        self.user_repository: UserRepository = user_repository
        self.token_processor: TokenProcessorUseCase = token_processor

    async def login(self, username: str, password: str, db_session: AsyncSession) -> TokenSchema:
        user = await self.__autenticate_user(username, password, db_session)
        roles = await self.user_repository.get_roles_by_user_id(user.id, db_session)
        token = await self.token_processor.generate_tokens(user.id, user.username, roles)
        return token

    async def logout(self, user_id: int, db_session: AsyncSession):
        pass

    async def __autenticate_user(self, username: str, password: str, db_session: AsyncSession):
        # first check whether user exists
        user = await self.user_repository.get_user_by_username(username, db_session)

        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        # now check the password
        isPasswordValid = verify_password(password, user.password)
        if not isPasswordValid:
            raise HTTPException(status_code=401, detail="Unauthorized")

        if not user.is_active:
            raise HTTPException(status_code=401, detail="User not active yet")

        return user


