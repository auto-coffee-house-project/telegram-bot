import httpx

__all__ = ('ServerAPIError',)


class ServerAPIError(Exception):
    """Raised when returned internal server error"""

    def __init__(self, response: httpx.Response):
        self.response = response
