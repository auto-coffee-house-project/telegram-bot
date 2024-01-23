from pydantic import TypeAdapter

from exceptions import ServerAPIError
from models import Bot
from parsers import parse_api_response
from repositories.base import APIRepository

__all__ = ('BotRepository',)


class BotRepository(APIRepository):

    async def get_all(self) -> list[Bot]:
        url = '/telegram/bots/'
        response = await self._http_client.get(url)

        api_response = parse_api_response(response)

        if api_response.ok:
            type_adapter = TypeAdapter(list[Bot])
            return type_adapter.validate_python(api_response.result)

        raise ServerAPIError(response)
