from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.constant.http_status_code import HttpStatusCode


async def handle_http_exception(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


async def handle_custom_exception(request, exc):
    http_status_code = exc.http_status_code.value[0]
    return JSONResponse(
        status_code=http_status_code,
        content={"message": exc.args[0]},
    )


async def handle_generic_exception(request, exc):
    return JSONResponse(
        status_code=HttpStatusCode.INTERNAL_SERVER_ERROR.value[0],
        content={"message": "Internal Server Error"},
    )


class CustomExceptionHandler:
    def __init__(self, app):
        self.app = app

    async def __call__(self, request, exc):
        if isinstance(exc, HTTPException):
            return await handle_http_exception(request, exc)
        elif isinstance(exc, (UnprocessableEntityException,
                              InternalServerErrorException, BadRequestException, ConflictException,
                              DataNotFoundException, ForbiddenException, ServiceUnavailableException,
                              UnauthorizedException
                              )):
            return await handle_custom_exception(request, exc)
        else:
            return await handle_generic_exception(request, exc)


class UnprocessableEntityException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.http_status_code = HttpStatusCode.UNPROCESSABLE_ENTITY


class InternalServerErrorException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.http_status_code = HttpStatusCode.INTERNAL_SERVER_ERROR


class BadRequestException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.http_status_code = HttpStatusCode.BAD_REQUEST


class ConflictException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.http_status_code = HttpStatusCode.CONFLICT


class DataNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.http_status_code = HttpStatusCode.NOT_FOUND


class ForbiddenException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.http_status_code = HttpStatusCode.FORBIDDEN


class ServiceUnavailableException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.http_status_code = HttpStatusCode.SERVICE_UNAVAILABLE


class UnauthorizedException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.http_status_code = HttpStatusCode.UNAUTHORIZED
