from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import UserIsEmployeeError, ClientAlreadyHasGiftError

__all__ = ('router',)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(UserIsEmployeeError))
async def on_user_is_employee_error(event: ErrorEvent):
    await event.update.message.answer(
        text='❌ Пользователь является сотрудником этой сети',
    )


@router.error(ExceptionTypeFilter(ClientAlreadyHasGiftError))
async def on_client_already_has_gift_error(event: ErrorEvent):
    await event.update.message.answer(
        text='❌ Вы не можете отсканировать код'
             ' клиента пока он ещё не забрал свой подарок',
    )
