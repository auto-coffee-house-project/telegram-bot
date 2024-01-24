from exceptions import ServerAPIError, AdminDoesNotExistError
from models import Admin
from parsers import parse_api_response
from repositories.base import APIRepository

__all__ = ('AdminRepository',)


class AdminRepository(APIRepository):

    async def get_by_user_id(self, user_id: int) -> Admin:
        url = f'/admins/{user_id}/'
        response = await self._http_client.get(url)
        api_response = parse_api_response(response)

        if api_response.ok:
            return Admin.model_validate(api_response.result)

        if api_response.message == 'Does not exist':
            raise AdminDoesNotExistError(user_id)

        raise ServerAPIError(response)
