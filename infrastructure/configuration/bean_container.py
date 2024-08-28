from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, Container, inject

from app.core.usecases.impl.token_processor_usercase_impl import TokenProcessorUseCaseImpl
from app.core.usecases.token_processor_usecase import TokenProcessorUseCase
from infradetails.gateways.base_token_gateway import BaseTokenGateway
from infradetails.gateways.impls.token_gateway_impl import TokenGatewayImpl
from infradetails.gateways.test_gateway import TestGateway
from infradetails.gateways.test_gateway_2 import TestGateway2


class TokenProcessorUseCaseContainer(containers.DeclarativeContainer):
    base_token_gateway = providers.Singleton(TokenGatewayImpl)

    token_processor_usecase = providers.Singleton(TokenProcessorUseCaseImpl, keycloak=base_token_gateway)

class TestContainer(containers.DeclarativeContainer):
    test_gateway = providers.Singleton(TestGateway, name = "prince")

class TestContainer2(containers.DeclarativeContainer):
    test_container = providers.Container(TokenProcessorUseCaseContainer)
    test_gateway2 = providers.Singleton(TestGateway2, token_gateway = test_container.token_processor_usecase)


class MainContainer(containers.DeclarativeContainer):
    test = providers.Container(
        TestContainer
    )
    infra = providers.Container(
        TokenProcessorUseCaseContainer
    )
    test2 = providers.Container(
        TestContainer2
    )

