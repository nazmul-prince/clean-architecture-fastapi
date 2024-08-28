import logging
import typing

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from app.core.exception.global_exception_handler import CustomExceptionHandler
from infrastructure.configuration.api_validation_bean_container import ApiValidationContainer
from infrastructure.configuration.auth_and_token_bean_config import AuthAndTokenProcessorUseCaseContainer
from infrastructure.configuration.bean_container import MainContainer
from infrastructure.configuration.middleware import configure_middleware
from infrastructure.configuration.security.router_interceptor import RouterInterceptor
from infrastructure.configuration.user_bean_container import UserUseCaseMainContainer
from infrastructure.lifespan_manager import lifespan
from infrastructure.routes import authentication_controller, user_controller, role_controller
from infrastructure.routes.api_router import router
from infrastructure.routes import authentication_controller
from fastapi_keycloak_middleware import KeycloakConfiguration, setup_keycloak_middleware, AuthorizationMethod

# logging.config.dictConfig(LOGGING_CONFIG)

load_dotenv()


def create_app() -> FastAPI:
    app = FastAPI(
        title="API Documentation",
        description="Event management service",
        version="0.1.0",
        lifespan=lifespan,
        debug=True
    )

    # Container().wire(modules=[authentication_controller])
    container = MainContainer()
    container.wire(modules=[authentication_controller])
    user_usecase_container = UserUseCaseMainContainer()
    user_usecase_container.wire(modules=[user_controller, role_controller])

    auth_and_token_usercase_container = AuthAndTokenProcessorUseCaseContainer()
    auth_and_token_usercase_container.wire(modules=[authentication_controller])

    api_validation_container = ApiValidationContainer()
    api_validation_container.wire(modules=[user_controller])
    # container.init_resources()
    # container.wire(modules=["infrastructure.routes.authentication_controller"])
    # app.container = container

    # customize_openapi(app)

    return app


# def customize_openapi(app: FastAPI):
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = app.openapi()
#
#     # Define the security scheme
#     security_scheme = SecuritySchemeModel(
#         type="oauth2",
#         flows=OAuthFlowsModel(password=OAuthFlowPassword(tokenUrl="token")),
#     )
#
#     # Add the security scheme to the openapi schema
#     openapi_schema["components"]["securitySchemes"] = {"OAuth2PasswordBearer": security_scheme}
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


app = create_app()

# Exception handler
exception_handler = CustomExceptionHandler(app)
app.add_exception_handler(Exception, exception_handler)

# Routes
app.include_router(router)

# Configure middleware
configure_middleware(app)

# app.router.route_class = RouterInterceptor

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=7711, workers=1)
