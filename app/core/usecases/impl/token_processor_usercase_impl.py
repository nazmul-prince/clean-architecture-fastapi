from datetime import datetime
from typing import Dict, List

from asyncpg.pgproto.pgproto import timedelta
from app.core.schema.authentication_schema import TokenSchema
from app.core.usecases.token_processor_usecase import TokenProcessorUseCase
from infradetails.gateways.base_token_gateway import BaseTokenGateway
import logging
import jwt

from infradetails.repositories.user_repository import UserRepository
from infrastructure.configuration.consts.token_configs import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, \
    SECRET_KEY, ALGORITHM


class TokenProcessorUseCaseImpl(TokenProcessorUseCase):

    def __init__(self):
        pass

    async def fetch_token(self, subject_token: str) -> TokenSchema:
        pass

    async def fetch_access_token_using_refresh_token(self, refresh_token: str) -> TokenSchema:
        pass

    async def generate_tokens(self, user_id: int, username: str, roles: List[str]) -> TokenSchema:
        access_token_expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        access_token = self.__create_access_token(data={"sub": str(username), "user_id": str(user_id), "roles": roles},
                                                  expires_in=access_token_expires)
        refresh_token = self.__create_refresh_token(data={"sub": str(username), "user_id": str(user_id)},
                                                    expires_in=refresh_token_expires)
        return TokenSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            toke_type="Bearer",
            access_token_expires_in = int(access_token_expires.timestamp() * 1000),
            refresh_token_expires_in = int(refresh_token_expires.timestamp() * 1000)
        )

    async def regenerate_tokens_with_refresh_token(self, refresh_token: str) -> TokenSchema:
        pass

    async def __refresh_access_token(self, refresh_token: str) -> str:
        pass

    def __create_access_token(self, data: Dict, expires_in: datetime) -> str:
        to_encode = data.copy()
        to_encode.update({"exp": expires_in})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def __create_refresh_token(self, data: Dict, expires_in: datetime) -> str:
        to_encode = data.copy()
        to_encode.update({"exp": expires_in})
        refresh_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return refresh_jwt

    def printTest(self):
        logging.info("printing testtttt")
