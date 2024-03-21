from exceptions import ServerAPIError
from exceptions.codes import CodeDoesNotExistError
from parsers import parse_api_response
from repositories.base import APIRepository

__all__ = ('GiftRepository',)


class GiftRepository(APIRepository):

    async def activate_code(self, *, code: str, employee_user_id: int) -> None:
        url = '/shops/gift-codes/activate/'
        request_data = {'code': code, 'employee_user_id': employee_user_id}

        response = await self._http_client.post(url, json=request_data)

        api_response = parse_api_response(response)

        if api_response.ok:
            return

        if api_response.message == 'Does not exist':
            raise CodeDoesNotExistError(code)

        raise ServerAPIError(response)
