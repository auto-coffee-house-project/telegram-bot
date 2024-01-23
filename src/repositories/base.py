import httpx

__all__ = ('APIRepository',)


class APIRepository:

    __slots__ = ('_http_client',)

    def __init__(self, http_client: httpx.AsyncClient):
        self._http_client = http_client
