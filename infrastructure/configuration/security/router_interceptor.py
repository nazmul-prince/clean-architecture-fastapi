import time
from typing import Callable

from fastapi.routing import APIRoute
from starlette.responses import Response

from starlette.requests import Request

from infrastructure.configuration.security.auth_permission_validator import AuthPermissionValidator


class RouterInterceptor(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            # Log request details before processing

            path = request.scope.get("route").path
            print(f"Handling request: {request.method} {request.url.path}")
            start_time = time.time()
            await AuthPermissionValidator.validate_permission(request)
            # Call the original route handler
            response: Response = await original_route_handler(request)

            # Log response details after processing
            duration = time.time() - start_time
            print(f"Completed request: {response.status_code} in {duration:.4f} seconds")

            return response

        return custom_route_handler
