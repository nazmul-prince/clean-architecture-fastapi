from fastapi import FastAPI
from fastapi_keycloak_middleware import KeycloakConfiguration, AuthorizationMethod, setup_keycloak_middleware

from infrastructure.settings.settings import settings
# set up keycloak middleware
# Set up Keycloak
async def scope_mapper(claim_auth) -> typing.List[str]:
    """
    Map token roles to internal permissions.

    This could be whatever code you like it to be, you could also fetch this
    from database. Keep in mind this is done for every incoming request though.
    """
    permissions = []

    return permissions

keycloak_config = KeycloakConfiguration(
    url=settings.keycloak_base_url,
    realm=settings.keycloak_realm,
    client_id=settings.client_id,
    reject_on_missing_claim=False,
    authorization_method=AuthorizationMethod.CLAIM,
)

def add_keycloak_middleware(app: FastAPI):
    setup_keycloak_middleware(
        app,
        keycloak_configuration=keycloak_config,
        # scope_mapper=scope_mapper,
    )