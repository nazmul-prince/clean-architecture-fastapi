from abc import ABCMeta, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schema.token_schema import TokenSchema


class AuthenticatorRepository(metaclass=ABCMeta):

    @abstractmethod
    def login(self, db_session: AsyncSession) -> TokenSchema:
        pass

    @abstractmethod
    def logout(self, db_session: AsyncSession) -> None:
        pass

    @abstractmethod
    def fetch_access_token_with_refresh_token(self,
                                              refresh_token: str,
                                              db_session: AsyncSession) -> None:
        pass