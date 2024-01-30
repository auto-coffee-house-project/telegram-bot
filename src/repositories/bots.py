from pydantic import TypeAdapter

from exceptions import ServerAPIError, BotDoesNotExistError
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

    async def get_by_id(self, bot_id: int) -> Bot:
        url = f'/telegram/bots/{bot_id}/'
        response = await self._http_client.get(url)

        api_response = parse_api_response(response)

        if api_response.ok:
            return Bot.model_validate(api_response.result)

        if api_response.message == 'Does not exist':
            raise BotDoesNotExistError(bot_id)

        raise ServerAPIError(response)
