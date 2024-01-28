from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import (
    ServerAPIError,
    ResponseJSONParseError,
    SalesmanDoesNotExistError,
    SalesmanAndSaleCodeShopGroupsNotEqualError,
)
from exceptions.codes import CodeDoesNotExistError, CodeExpiredError

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(SalesmanAndSaleCodeShopGroupsNotEqualError))
async def on_salesman_and_sale_code_shop_groups_not_equal_error(
        event: ErrorEvent,
) -> None:
    if event.update.message is not None:
        await event.update.message.reply(
            '❌ Вы не являетесь продавцом в данной сети кофеен',
        )
        return
    raise event.exception


@router.error(ExceptionTypeFilter(CodeExpiredError))
async def on_code_expired_error(event: ErrorEvent) -> None:
    if event.update.message is not None:
        await event.update.message.reply('❌ Истек срок действия кода')
        return
    raise event.exception


@router.error(ExceptionTypeFilter(SalesmanDoesNotExistError))
async def on_salesman_does_not_exist_error(event: ErrorEvent) -> None:
    if event.update.message is not None:
        await event.update.message.reply('❌ Вы не являетесь продавцом')
        return
    raise event.exception


@router.error(ExceptionTypeFilter(CodeDoesNotExistError))
async def on_code_does_not_exist_error(event: ErrorEvent) -> None:
    if event.update.message is not None:
        await event.update.message.reply('❌ Код не найден')
        return
    raise event.exception


@router.error(ExceptionTypeFilter(ServerAPIError))
async def on_server_api_error(event: ErrorEvent) -> None:
    if event.update.message is not None:
        await event.update.message.answer('Произошла ошибка на сервере')
        return
    raise event.exception


@router.error(ExceptionTypeFilter(ResponseJSONParseError))
async def on_response_json_parse_error(event: ErrorEvent) -> None:
    if event.update.message is not None:
        await event.update.message.answer(
            'Произошла ошибка при обработке ответа от сервера')
        return
    raise event.exception
