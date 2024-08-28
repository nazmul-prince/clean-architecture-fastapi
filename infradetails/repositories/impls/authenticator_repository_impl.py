from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schema.token_schema import TokenSchema
from infradetails.repositories.authentor_repository import AuthenticatorRepository


class AuthenticatorRepositoryImpl(AuthenticatorRepository):
    def login(self, db_session: AsyncSession) -> TokenSchema:
        pass

    def logout(self, db_session: AsyncSession) -> None:
        pass

    def fetch_access_token_with_refresh_token(self, refresh_token: str, db_session: AsyncSession) -> None:
        pass