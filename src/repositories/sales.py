from pydantic import TypeAdapter

from exceptions import (
    ClientAlreadyHasGiftError, SaleDeletionTimeExpiredError,
    SalesmanAndSaleCodeShopGroupsNotEqualError,
    SalesmanDoesNotExistError, ServerAPIError, UserIsEmployeeError,
)
from exceptions.codes import CodeDoesNotExistError, CodeExpiredError
from models import ClientPurchasesStatistics, Sale
from parsers import parse_api_response
from repositories.base import APIRepository

__all__ = ('SaleRepository',)


class SaleRepository(APIRepository):

    async def create_by_user_id(
            self,
            *,
            client_user_id: int,
            employee_user_id: int,
    ) -> Sale:
        url = '/shops/sales/by-users/'
        request_data = {
            'client_user_id': client_user_id,
            'employee_user_id': employee_user_id,
        }

        response = await self._http_client.post(url, json=request_data)

        api_response = parse_api_response(response)

        if api_response.ok:
            return Sale.model_validate(api_response.result)

        if api_response.message == 'Client already has gift':
            raise ClientAlreadyHasGiftError

        if api_response.message == 'User is employee':
            raise UserIsEmployeeError

        raise ServerAPIError(response)

    async def create_by_code(
            self,
            *,
            code: str,
            employee_user_id: int,
    ) -> Sale:
        url = '/shops/sales/by-codes/'
        request_data = {
            'code': code,
            'employee_user_id': employee_user_id,
        }

        response = await self._http_client.post(url, json=request_data)

        api_response = parse_api_response(response)

        if api_response.ok:
            return Sale.model_validate(api_response.result)

        error_message = api_response.message

        if error_message == 'User is employee':
            raise UserIsEmployeeError

        if error_message == 'Does not exist':
            if 'code' in api_response.extra:
                raise CodeDoesNotExistError(api_response.extra['code'])
            if 'user_id' in api_response.extra:
                raise SalesmanDoesNotExistError(api_response.extra['user_id'])

        if error_message == 'Sale temporary code expired':
            raise CodeExpiredError(code)

        if error_message == 'Salesman and sale code shop groups not equal':
            raise SalesmanAndSaleCodeShopGroupsNotEqualError(
                salesman_user_id=employee_user_id,
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
