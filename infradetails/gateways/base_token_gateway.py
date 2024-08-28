from abc import ABC, abstractmethod

from app.core.schema.authentication_schema import TokenSchema


class BaseTokenGateway(ABC):
    @abstractmethod
    async def fetch_token(self, subject_token: str) -> TokenSchema:
        pass

    @abstractmethod
    async def fetch_access_token_using_refresh_token(self, refresh_token: str) -> TokenSchema:
        pass

    @abstractmethod
    async def introspect_token(self, token: str):
        pass