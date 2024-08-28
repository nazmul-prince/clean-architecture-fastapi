from dependency_injector import containers, providers

from app.core.usecases.impl.auth_usecase_impl import AuthUsecaseImpl
from app.core.usecases.impl.token_processor_usercase_impl import TokenProcessorUseCaseImpl
from infrastructure.configuration.user_bean_container import UserRepositoryContainer


class AuthAndTokenProcessorUseCaseContainer(containers.DeclarativeContainer):

    token_processor_usecase = providers.Singleton(TokenProcessorUseCaseImpl)
    user_repo_container = providers.Container(UserRepositoryContainer)
    auth_usecase = providers.Singleton(AuthUsecaseImpl, user_repository = user_repo_container.user_repository, token_processor = token_processor_usecase)