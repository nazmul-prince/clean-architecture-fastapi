from typing import List

import jwt
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import logging

from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Request

from app.core.usecases.api_validation import ApiValidator
from infrastructure.configuration.consts.token_configs import SECRET_KEY, ALGORITHM
from infrastructure.configuration.security.role_map import ROLE_MAPS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthPermissionValidator:

    @staticmethod
    async def validate_permission(request: Request):
        path = request.scope.get("route").path
        method = request.method

        route_requirements = ROLE_MAPS.get(path, {}).get(method, {})

        if route_requirements:
            required_roles = route_requirements.get("required_roles", [])
            extra_validator: ApiValidator = route_requirements.get("extra_validator", None)
            logging.info(path)

            # if path in ROLE_MAPS:
            token = await oauth2_scheme(request)

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
                user_roles: List[str] = payload.get("roles", [])

                if not any(role in user_roles for role in required_roles):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="You do not have access to this resource",
                    )
                if extra_validator:
                    await extra_validator.validateApiRoute()
            except RuntimeError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials"
                )
