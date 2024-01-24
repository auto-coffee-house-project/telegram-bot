from exceptions import ServerAPIError, BotDoesNotExistError
from models import SaleGroup
from parsers import parse_api_response
from repositories.base import APIRepository

__all__ = ('ShopGroupRepository',)


class ShopGroupRepository(APIRepository):

    async def get_by_bot_id(self, bot_id: int) -> SaleGroup:
        url = f'/shops/groups/bots/{bot_id}/'
        response = await self._http_client.get(url)

        api_response = parse_api_response(response)

        if api_response.ok:
            return SaleGroup.model_validate(api_response.result)

        if api_response.message == 'Does not exist':
            raise BotDoesNotExistError(bot_id)

        raise ServerAPIError(response)
