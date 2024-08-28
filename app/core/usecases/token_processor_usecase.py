from abc import ABCMeta
from abc import  abstractmethod
from typing import List

from app.core.schema.authentication_schema import TokenSchema


class TokenProcessorUseCase(metaclass=ABCMeta):

    @abstractmethod
    async def fetch_token(self, subject_token: str) -> TokenSchema:
        pass

    @abstractmethod
    async def fetch_access_token_using_refresh_token(self, refresh_token: str) -> TokenSchema:
        pass

    @abstractmethod
    async def generate_tokens(self,  user_id: int, username: str, roles: List[str]) -> TokenSchema:
        pass

    @abstractmethod
    async def regenerate_tokens_with_refresh_token(self, refresh_token: str):
        pass

    @abstractmethod
    async def printTest(self):
        pass
