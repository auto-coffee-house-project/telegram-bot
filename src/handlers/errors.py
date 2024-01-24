from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import ServerAPIError, ResponseJSONParseError

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(ServerAPIError))
async def on_server_api_error(event: ErrorEvent, **kwargs) -> None:
    print(kwargs)


@router.error(ExceptionTypeFilter(ResponseJSONParseError))
async def on_response_json_parse_error(event: ErrorEvent, **kwargs) -> None:
    print(kwargs)
