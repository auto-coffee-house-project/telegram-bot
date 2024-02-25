from aiogram import Router, F, Bot
from aiogram.enums import ChatType
from aiogram.filters import StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import (
    code_input_filter,
    user_is_salesman_filter,
    user_is_admin_filter,
)
from models import User
from repositories import SaleRepository
from views import SaleCodeSuccessfullyAppliedView, answer_view

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
async def on_ask_for_sale_temporary_code(message: Message) -> None:
    await message.answer('✏️ Введи код')


@router.message(
    F.chat.type == ChatType.PRIVATE,
    code_input_filter,
    or_f(
        user_is_salesman_filter,
        user_is_admin_filter,
    ),
    StateFilter('*'),
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
    await sale_repository.create_by_code(
        code=code,
        employee_user_id=user.id,
    )
