from functools import wraps
from typing import List, Callable, Optional

import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.usecases.api_validation import ApiValidator
from infrastructure.configuration.consts.token_configs import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_roles_from_token(token: str) -> List[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        roles: List[str] = payload.get("roles", [])
        return roles
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized token"
        )


def has_roles(required_roles: List[str], api_validator: Optional[ApiValidator] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            token: str = kwargs.get("token")
            roles = get_roles_from_token(token)

            if not any(role in roles for role in required_roles):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized, didn't have enough permission"
                )
            if api_validator:
                await api_validator.validateApiRoute()

            return await func(*args, **kwargs)

        return wrapper
    return decorator
