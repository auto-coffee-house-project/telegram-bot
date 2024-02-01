from uuid import UUID

from exceptions import (
    ServerAPIError,
    InvitationExpiredError,
    InvitationDoesNotExistError,
    SalesmanDoesNotExistError,
    SalesmanAlreadyExistsError,
    UserIsAlreadyAdminError,
)
from models import SalesmanCreateResponse, ShopSalesmans
from parsers import parse_api_response
from repositories.base import APIRepository

__all__ = ('SalesmanRepository',)


class SalesmanRepository(APIRepository):

    async def get_all(self, admin_user_id: int) -> ShopSalesmans:
        url = '/shops/salesmans/'
        request_query_params = {'admin_user_id': admin_user_id}

        response = await self._http_client.get(url, params=request_query_params)

        api_response = parse_api_response(response)

        if api_response.ok:
            return ShopSalesmans.model_validate(api_response.result)

        raise ServerAPIError(response)

    async def create(
            self,
            *,
            invitation_id: UUID,
            user_id: int,
    ) -> SalesmanCreateResponse:
        url = '/shops/salesmans/'
        request_data = {
            'invitation_id': str(invitation_id),
            'user_id': user_id,
        }

        response = await self._http_client.post(url, json=request_data)

        api_response = parse_api_response(response)

        if api_response.ok:
            return SalesmanCreateResponse.model_validate(api_response.result)

        if api_response.message == 'Does not exist':
            raise InvitationDoesNotExistError

        if api_response.message == 'Salesman invitation expired':
            raise InvitationExpiredError

        if api_response.message == 'User is already salesman':
            raise SalesmanAlreadyExistsError

        if api_response.message == 'User is already shop admin':
            raise UserIsAlreadyAdminError

        raise ServerAPIError(response)

    async def delete_by_user_id(self, user_id: int) -> None:
        url = f'/shops/salesmans/{user_id}/'

        response = await self._http_client.delete(url)

        api_response = parse_api_response(response)

        if api_response.ok:
            return

        if api_response.message == 'Object does not exist':
            raise SalesmanDoesNotExistError

        raise ServerAPIError(response)
