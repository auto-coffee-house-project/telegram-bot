from exceptions import ServerAPIError
from parsers import parse_api_response
from repositories.base import APIRepository

__all__ = ('MailingRepository',)


class MailingRepository(APIRepository):

    async def create(self, text: str, bot_id: int, admin_user_id: int) -> None:
        url = '/shops/mailings/'
        request_data = {
            'text': text,
            'admin_user_id': admin_user_id,
            'bot_id': bot_id,
        }
        response = await self._http_client.post(url, json=request_data)

        api_response = parse_api_response(response)

        if api_response.ok:
            return

        raise ServerAPIError(response)
