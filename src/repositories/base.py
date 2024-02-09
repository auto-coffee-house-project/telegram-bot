import httpx
from models import APIResponse
from exceptions import BotDoesNotExistError

__all__ = ('APIRepository', 'handle_common_errors')


class APIRepository:
    __slots__ = ('_http_client',)

    def __init__(self, http_client: httpx.AsyncClient):
        self._http_client = http_client


def handle_common_errors(api_response: APIResponse) -> None:
    if api_response.message == 'Does not exist':
        if api_response.extra and 'bot_id' in api_response.extra:
            raise BotDoesNotExistError
