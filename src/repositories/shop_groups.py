from models import SaleGroup
from repositories.base import APIRepository

__all__ = ('ShopGroupRepository',)


class ShopGroupRepository(APIRepository):

    async def get_by_bot_id(self, bot_id: int) -> SaleGroup:
        url = f'/shops/groups/bots/{bot_id}/'
        response = await self._http_client.get(url)
        return SaleGroup.model_validate(response.json())
