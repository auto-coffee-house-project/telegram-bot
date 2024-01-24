from aiogram.types import User as TelegramUser

from exceptions import ServerAPIError
from models import User
from parsers import parse_api_response
from repositories.base import APIRepository

__all__ = ('UserRepository',)


class UserRepository(APIRepository):

    async def upsert_user(self, user: TelegramUser) -> User:
        url = '/telegram/users/'
        request_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
        }
        response = await self._http_client.post(url, json=request_data)

        api_response = parse_api_response(response)

        if api_response.ok:
            return User.model_validate(api_response.result)

        raise ServerAPIError(response)
