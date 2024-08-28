import logging

from app.core.usecases.api_validation import ApiValidator


class UserActivationApiValidation(ApiValidator):

    async def validateApiRoute(self, *args, **kwargs):
        logging.info("validating route for api /users/{user_id}/activate")
