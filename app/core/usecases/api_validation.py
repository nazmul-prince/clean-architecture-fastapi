from abc import ABC, abstractmethod


class ApiValidator(ABC):

    @abstractmethod
    async def validateApiRoute(self, *args, **kwargs):
        pass