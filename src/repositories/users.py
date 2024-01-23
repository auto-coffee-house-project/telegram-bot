from aiogram.types import User as TelegramUser

from repositories.base import APIRepository

__all__ = ('UserRepository',)


class UserRepository(APIRepository):

    async def get_or_create(self, user: TelegramUser) -> tuple[dict, bool]:
        try:
            return await self.get_by_id(user.id), False
        except Exception:  # TODO specify exception
            return await self.create(user), True

    async def get_by_id(self, user_id: int) -> dict:
        url = f'/users/{user_id}/'
        response = await self._http_client.get(url)
        # TODO check response
        return response.json()

    async def create(self, user: TelegramUser) -> dict:
        url = '/users/'
        request_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
        }
        response = await self._http_client.post(url=url, json=request_data)
        # TODO check response
        return response.json()
