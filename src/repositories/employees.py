from uuid import UUID

from exceptions import (
    InvitationDoesNotExistError,
    InvitationExpiredError,
    SalesmanAlreadyExistsError,
    ServerAPIError,
    UserIsAlreadyAdminError,
)
from models import SalesmanCreateResponse
from parsers import parse_api_response
from repositories.base import APIRepository

__all__ = ('EmployeeRepository',)


class EmployeeRepository(APIRepository):

    async def create(
            self,
            *,
            invitation_id: UUID,
            user_id: int,
    ) -> SalesmanCreateResponse:
        url = '/shops/employees/'
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
