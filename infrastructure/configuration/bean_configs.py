from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from sqlalchemy.sql.operators import contains
from dependency_injector import containers, providers

from app.core.usecases.impl.token_processor_usercase_impl import TokenProcessorUseCaseImpl
from app.core.usecases.token_processor_usecase import TokenProcessorUseCase
from infradetails.gateways.impls.token_gateway_impl import TokenGatewayImpl


def get_base_tokey_gateway():
    return TokenGatewayImpl()

def get_token_processor_usecase(token_gateway: TokenProcessorUseCase = Depends(get_base_tokey_gateway)):
    return TokenProcessorUseCaseImpl(token_gateway)
