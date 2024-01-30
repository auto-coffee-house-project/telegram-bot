from aiogram import Router, F, Bot
from aiogram.enums import ChatType
from aiogram.filters import StateFilter, invert_f, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import (
    code_input_filter, user_is_salesman_filter,
    user_is_admin_filter
)
from models import User
from repositories import SaleRepository
from services.notifiers import send_code_applied_notification
from states import SaleTemporaryCodeStates
from views import SaleTemporaryCodeSuccessfullyAppliedView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.chat.type == ChatType.PRIVATE,
    F.text == '📲 Ввести код вручную',
    or_f(
        user_is_salesman_filter,
        user_is_admin_filter,
    ),
    StateFilter('*'),
)
async def on_ask_for_sale_temporary_code(
        message: Message,
        state: FSMContext,
) -> None:
    await state.set_state(SaleTemporaryCodeStates.code)
    await message.answer('✏️ Введи код')


@router.message(
    F.chat.type == ChatType.PRIVATE,
    invert_f(code_input_filter),
    or_f(
        user_is_salesman_filter,
        user_is_admin_filter,
    ),
    StateFilter(SaleTemporaryCodeStates.code),
)
async def on_sale_temporary_code_invalid_input(
        message: Message,
) -> None:
    await message.reply('❌ Код должен состоять из 4 цифр')


@router.message(
    F.chat.type == ChatType.PRIVATE,
    code_input_filter,
    or_f(
        user_is_salesman_filter,
        user_is_admin_filter,
    ),
    StateFilter(SaleTemporaryCodeStates.code),
)
async def on_sale_temporary_code_input(
        message: Message,
        state: FSMContext,
        sale_repository: SaleRepository,
        code: str,
        user: User,
        bot: Bot,
) -> None:
    await state.clear()
    sale = await sale_repository.create(
        code=code,
        salesman_user_id=user.id,
    )
    view = SaleTemporaryCodeSuccessfullyAppliedView(sale)
    await answer_view(message, view)
    await send_code_applied_notification(
        bot=bot,
        sale=sale,
    )
