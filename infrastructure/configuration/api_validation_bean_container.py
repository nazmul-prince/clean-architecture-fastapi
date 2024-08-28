from dependency_injector import containers, providers

from app.core.usecases.impl.user_activation_api_validation_impl import UserActivationApiValidation


class ApiValidationContainer(containers.DeclarativeContainer):
    user_activation_validator = providers.Singleton(UserActivationApiValidation)