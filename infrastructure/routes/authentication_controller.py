import fastapi
import logging
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Form
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing.plugin.plugin_base import logging

from app.core.usecases.auth_usecase import AuthUsecase
from app.core.usecases.impl.token_processor_usercase_impl import TokenProcessorUseCaseImpl
from infradetails.gateways.impls.token_gateway_impl import TokenGatewayImpl
from infradetails.gateways.keycloak_manager import fetch_token, fetch_access_token_using_refresh_token
from infradetails.gateways.test_gateway import TestGateway
from infradetails.gateways.test_gateway_2 import TestGateway2
from infrastructure.configuration.auth_and_token_bean_config import AuthAndTokenProcessorUseCaseContainer
from infrastructure.configuration.bean_configs import get_token_processor_usecase
from infrastructure.configuration.bean_container import TokenProcessorUseCaseContainer, MainContainer
from infrastructure.configuration.db_config import get_async_db
from app.core.schema.authentication_schema import TokenExchangeRequestSchema, TokenSchema, \
    NewTokenRequestSchema
from app.core.usecases.token_processor_usecase import TokenProcessorUseCase

router = fastapi.APIRouter(prefix="/event-management/api/v1/public")


@router.post("/token-exchange", response_model=TokenSchema, tags=["Authentication"])
async def exchange_token(
        token_request: TokenExchangeRequestSchema,
        db: AsyncSession = Depends(get_async_db)
):
    # result = token_processor_usecase.fetch_token(subject_token=token_request.subject_token)
    # result = await fetch_token(
    #     subject_token=token_request.subject_token,
    # )

    return JSONResponse(content=jsonable_encoder(None))


@router.post("/token-old", response_model=TokenSchema, tags=["Authentication"])
@inject
async def fetch_new_token(
        token_request: NewTokenRequestSchema,
        db: AsyncSession = Depends(get_async_db),
        token_processor: TokenProcessorUseCaseImpl = Depends(Provide[MainContainer.infra.token_processor_usecase]),
        test: TestGateway = Depends(Provide[MainContainer.test.test_gateway]),
        test2: TestGateway2 = Depends(Provide[MainContainer.test2.test_gateway2])
):
    test.get_name()
    test2.get_name()
    result =  await token_processor.fetch_access_token_using_refresh_token(refresh_token=token_request.refresh_token)
    return JSONResponse(content=jsonable_encoder(result))

@router.post("/token", response_model=TokenSchema, tags=["Authentication"])
@inject
async def login(
        username: str = Form(...),
        password: str = Form(...),
        db_session: AsyncSession = Depends(get_async_db),
        auth_usecase: AuthUsecase = Depends(Provide[AuthAndTokenProcessorUseCaseContainer.auth_usecase])
):
    token = await auth_usecase.login(username, password, db_session)
    return token
