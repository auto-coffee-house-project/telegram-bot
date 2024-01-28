from uuid import UUID

from exceptions import (
    ServerAPIError,
    InvitationExpiredError,
    InvitationDoesNotExistError,
)
from models import SalesmanCreateResponse
from parsers import parse_api_response
from repositories.base import APIRepository

__all__ = ('SalesmanRepository',)


class SalesmanRepository(APIRepository):

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

        if api_response.message == 'Object does not exist':
            raise InvitationDoesNotExistError

        if api_response.message == 'Salesman invitation expired':
            raise InvitationExpiredError

        raise ServerAPIError(response)
