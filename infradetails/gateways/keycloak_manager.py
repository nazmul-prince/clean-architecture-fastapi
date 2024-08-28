import logging
from typing import Optional, List

import aiohttp
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer

from app.core.schema.authentication_schema import TokenSchema
from infrastructure.settings.settings import settings


async def fetch_token(subject_token: str) -> TokenSchema:
    try:
        url = settings.keycloak_token_url
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': settings.client_id,
            'subject_token': subject_token,
            'grant_type': settings.grant_type,
            'subject_token_type': settings.subject_token_type,
            'subject_issuer': settings.subject_issuer,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status,
                                        detail=f"Error fetching token: {await response.text()}")

                response_data = await response.json()

                access_token = response_data.get("access_token")
                refresh_token = response_data.get("refresh_token")
                expires_in = response_data.get("expires_in")

                response = TokenSchema(
                    accessToken=access_token,
                    refreshToken=refresh_token,
                    expiresIn=expires_in
                )

                if not access_token or not refresh_token or expires_in is None:
                    raise HTTPException(status_code=500, detail="Incomplete token response from the server")

                return response
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"Error fetching new token using token exchange")


async def fetch_access_token_using_refresh_token(refresh_token: str) -> TokenSchema:
    try:
        url = settings.keycloak_token_url
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': settings.client_id,
            'grant_type': "refresh_token",
            'refresh_token': refresh_token,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status,
                                        detail=f"Error fetching new token: {await response.text()}")

                response_data = await response.json()

                response = TokenSchema(
                    accessToken=response_data.get("access_token"),
                    refreshToken=response_data.get("refresh_token"),
                    expiresIn=response_data.get("expires_in")
                )
                return response
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail=f"Error fetching new token")


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl=settings.keycloak_token_url,
    authorizationUrl=settings.keycloak_authorization_url
)


async def introspect_token(token: str):
    introspect_url = settings.keycloak_introspect_url
    introspect_data = {
        "client_id": settings.client_id,
        "client_secret": settings.client_secret,
        "token": token,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(introspect_url, data=introspect_data) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="Failed to introspect token")
            introspect_result = await response.json()

            if not introspect_result.get("active", False):
                raise HTTPException(status_code=401, detail="Invalid token")

            return introspect_result


def validate_token(required_roles: Optional[List[str]] = None,
                   required_permissions: Optional[List[str]] = None):
    async def _get_current_user_sub_and_check(token: str = Depends(oauth2_scheme)):
        token_data = await introspect_token(token)

        sub = token_data.get("sub")
        if not sub:
            raise HTTPException(status_code=500, detail="Missing 'sub' field in token")

        if required_roles:
            roles = token_data.get("roles")
            if roles is None:
                raise HTTPException(status_code=500, detail="Missing 'roles' field in token")

            if not any(role in roles for role in required_roles):
                raise HTTPException(status_code=403, detail="User does not have required roles")

        if required_permissions:
            permissions = token_data.get("permissions")
            if permissions is None:
                raise HTTPException(status_code=500, detail="Missing 'permissions' field in token")

            if not any(permission in permissions for permission in required_permissions):
                raise HTTPException(status_code=403, detail="User does not have required permissions")

        return sub

    return _get_current_user_sub_and_check
