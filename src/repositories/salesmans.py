from models import Salesman
from repositories.base import APIRepository

__all__ = ('SalesmanRepository',)


class SalesmanRepository(APIRepository):

    async def get_by_user_id(self, user_id: int) -> Salesman:
        url = f'/shops/salesmans/{user_id}/'
        response = await self._http_client.get(url)
        if response.status_code == 404:
            raise Exception
        return Salesman.model_validate(response.json())
