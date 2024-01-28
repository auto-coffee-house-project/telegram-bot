import httpx

__all__ = ('ResponseJSONParseError',)


class ResponseJSONParseError(Exception):

    def __init__(self, response: httpx.Response):
        self.response = response
