from exceptions import ServerAPIError, AdminDoesNotExistError
from models import Invitation
from parsers import parse_api_response
from repositories.base import APIRepository

__all__ = ('InvitationRepository',)


class InvitationRepository(APIRepository):

    async def create(self, admin_user_id: int) -> Invitation:
        url = '/shops/invitations/'
        request_data = {'admin_user_id': admin_user_id}
        response = await self._http_client.post(url, json=request_data)

        api_response = parse_api_response(response)

        if api_response.ok:
            return Invitation.model_validate(api_response.result)

        if api_response.message == 'Does not exist':
            raise AdminDoesNotExistError(admin_user_id)

        raise ServerAPIError(response)
