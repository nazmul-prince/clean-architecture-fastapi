from infrastructure.configuration.cors_config import get_cors_middleware
from infrastructure.configuration.keycloak_config import add_keycloak_middleware
from infrastructure.configuration.security.rbac_middleware import RBACMiddleware


def configure_middleware(app):
    app.add_middleware(get_cors_middleware)
    add_keycloak_middleware(app)
    # app.add_middleware(RBACMiddleware)
