from typing import Dict, List, Optional, Union

from app.core.usecases.api_validation import ApiValidator
from infrastructure.configuration.api_validation_bean_container import ApiValidationContainer

MethodRequirements = Dict[str, Union[List[str], Optional[ApiValidator]]]

# Define the type for route requirements
RouteRequirements = Dict[str, Dict[str, MethodRequirements]]

ROLE_MAPS: RouteRequirements = {
    "/event-management/api/v1/private/users/{user_id}/activate": {
        "GET": {
            "required_roles": ["admin"],
            "extra_validator": ApiValidationContainer.user_activation_validator()
        },
        "PUT": {
            "required_roles": ["admin", "user"],
            "extra_validator": ApiValidationContainer.user_activation_validator()
        },
    }
}
