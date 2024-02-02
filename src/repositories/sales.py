from pydantic import TypeAdapter

from exceptions import (
    ServerAPIError,
    SalesmanDoesNotExistError,
    SalesmanAndSaleCodeShopGroupsNotEqualError,
    SaleDeletionTimeExpiredError,
)
from exceptions.codes import CodeDoesNotExistError, CodeExpiredError
from models import Sale, ClientPurchasesStatistics
from parsers import parse_api_response
from repositories.base import APIRepository

__all__ = ('SaleRepository',)


class SaleRepository(APIRepository):

    async def create_by_user_id(
            self,
            client_user_id: int,
            salesman_user_id: int,
    ) -> Sale:
        url = '/shops/sales/users/'
        request_data = {
            'client_user_id': client_user_id,
            'salesman_user_id': salesman_user_id,
        }
        response = await self._http_client.post(url, json=request_data)

        api_response = parse_api_response(response)

        if api_response.ok:
            return Sale.model_validate(api_response.result)

        raise ServerAPIError(response)

    async def create_by_code(self, code: str, salesman_user_id: int) -> Sale:
        url = '/shops/sales/by-codes/'
        request_data = {
            'code': code,
            'salesman_user_id': salesman_user_id,
        }
        response = await self._http_client.post(url, json=request_data)

        api_response = parse_api_response(response)

        if api_response.ok:
            return Sale.model_validate(api_response.result)

        error_message = api_response.message

        if error_message == 'Does not exist':
            if 'code' in api_response.extra:
                raise CodeDoesNotExistError(api_response.extra['code'])
            if 'user_id' in api_response.extra:
                raise SalesmanDoesNotExistError(api_response.extra['user_id'])

        if error_message == 'Sale temporary code expired':
            raise CodeExpiredError(code)

        if error_message == 'Salesman and sale code shop groups not equal':
            raise SalesmanAndSaleCodeShopGroupsNotEqualError(
                salesman_user_id=salesman_user_id,
                code=code,
            )

        raise ServerAPIError(response)

    async def delete(self, sale_id: int) -> None:
        url = f'/shops/sales/{sale_id}/'
        response = await self._http_client.delete(url)

        api_response = parse_api_response(response)

        if api_response.ok:
            return

        if api_response.message == 'Sale deletion time expired':
            raise SaleDeletionTimeExpiredError

        raise ServerAPIError(response)

    async def get_statistics(
            self,
            *,
            bot_id: int,
    ) -> list[ClientPurchasesStatistics]:
        url = f'/shops/clients/all-statistics/'
        request_query_params = {'bot_id': bot_id}
        response = await self._http_client.get(url, params=request_query_params)

        api_response = parse_api_response(response)

        if api_response.ok:
            type_adapter = TypeAdapter(list[ClientPurchasesStatistics])
            return type_adapter.validate_python(api_response.result)

        raise ServerAPIError(response)
