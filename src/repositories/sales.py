from models import Sale
from repositories.base import APIRepository

__all__ = ('SaleRepository',)


class SaleRepository(APIRepository):

    async def create(self, code: str, salesman_user_id: int) -> Sale:
        url = '/shops/sales/'
        request_data = {
            'code': code,
            'salesman_user_id': salesman_user_id,
        }
        response = await self._http_client.post(url, json=request_data)
        return Sale.model_validate(response.json())
