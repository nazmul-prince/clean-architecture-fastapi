from dependency_injector import containers, providers

from app.core.usecases.impl.role_usecase_impl import RoleUseCaseImpl
from app.core.usecases.impl.user_usecase_impl import UserUseCaseImpl
from infradetails.repositories.impls.role_repository_impl import RoleRepositoryImpl
from infradetails.repositories.impls.user_repository_impl import UserRepositoryImpl
from infradetails.repositories.user_repository import UserRepository


class UserRepositoryContainer(containers.DeclarativeContainer):
    user_repository = providers.Singleton(UserRepositoryImpl)
    role_repository = providers.Singleton(RoleRepositoryImpl)

class UserUseCaseContainer(containers.DeclarativeContainer):
    user_repo_container = providers.Container(UserRepositoryContainer)
    user_usecase = providers.Singleton(UserUseCaseImpl, user_repository = user_repo_container.user_repository)
    role_usecase = providers.Singleton(RoleUseCaseImpl, role_repository = user_repo_container.role_repository)

class UserUseCaseMainContainer(containers.DeclarativeContainer):
    repos = providers.Container(UserRepositoryContainer)
    usecases = providers.Container(UserUseCaseContainer)