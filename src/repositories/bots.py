from pydantic import TypeAdapter

from exceptions import BotDoesNotExistError, ServerAPIError
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

    async def get_me(self) -> Bot:
        url = f'/telegram/bots/me/'

        response = await self._http_client.get(url)

        api_response = parse_api_response(response)

        if api_response.ok:
            return Bot.model_validate(api_response.result)

        if api_response.message == 'Does not exist':
            raise BotDoesNotExistError

        raise ServerAPIError(response)
