from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class AuthUsecase(ABC):

    @abstractmethod
    async def login(self, username: str, password: str, db_session: AsyncSession):
        pass

    @abstractmethod
    async def logout(self, user_id: int, db_session: AsyncSession):
        pass