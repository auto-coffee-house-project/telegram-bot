from exceptions import ServerAPIError, SalesmanDoesNotExistError
from models import Salesman
from parsers import parse_api_response
from repositories.base import APIRepository

__all__ = ('SalesmanRepository',)


class SalesmanRepository(APIRepository):

    async def get_by_user_id(self, user_id: int) -> Salesman:
        url = f'/shops/salesmans/{user_id}/'
        response = await self._http_client.get(url)

        api_response = parse_api_response(response)

        if api_response.ok:
            return Salesman.model_validate(api_response.result)

        if api_response.message == 'Does not exists':
            raise SalesmanDoesNotExistError(salesman_user_id=user_id)

        raise ServerAPIError(response)
