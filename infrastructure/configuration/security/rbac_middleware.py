from typing import List

import jwt
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import logging

from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Request

from infrastructure.configuration.consts.token_configs import SECRET_KEY, ALGORITHM
from infrastructure.configuration.security.role_map import ROLE_MAPS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class RBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        scope_route = request.scope.get("route")
        logging.info(scope_route)

        if scope_route in ROLE_MAPS:
            token = oauth2_scheme(request)

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
                user_roles: List[str] = payload.get("roles", [])
                required_roles = ROLE_MAPS[scope_route]

                if not any(role in user_roles for role in required_roles):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="You do not have access to this resource",
                    )
            except RuntimeError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials"
                )

        response = await call_next(request)
        return response



