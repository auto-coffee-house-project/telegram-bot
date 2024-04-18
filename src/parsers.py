import httpx
from pydantic import ValidationError

from exceptions import ResponseJSONParseError
from models import APIResponse

__all__ = ('parse_api_response',)


def parse_api_response(response: httpx.Response) -> APIResponse:
    try:
        return APIResponse.model_validate_json(response.text)
    except ValidationError:
        raise ResponseJSONParseError(response)
