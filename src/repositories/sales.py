from exceptions import (
    ServerAPIError, SalesmanDoesNotExistError,
    SalesmanAndSaleCodeShopGroupsNotEqualError
)
from exceptions.codes import CodeDoesNotExistError, CodeExpiredError
from models import Sale
from parsers import parse_api_response
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
