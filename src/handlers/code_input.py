from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter, invert_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import salesman_filter, code_input_filter
from models import Salesman
from repositories import SaleRepository
from states import SaleTemporaryCodeStates
from views import SaleTemporaryCodeSuccessfullyAppliedView, answer_view

router = Router(name=__name__)


@router.message(
    F.chat.type == ChatType.PRIVATE,
    F.text == '📲 Ввести код вручную',
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
    StateFilter('*'),
)
async def on_sale_temporary_code_invalid_input(
        message: Message,
) -> None:
    await message.reply('❌ Код должен состоять из 4 цифр')


@router.message(
    F.chat.type == ChatType.PRIVATE,
    code_input_filter,
    salesman_filter,
    StateFilter(SaleTemporaryCodeStates.code),
)
async def on_sale_temporary_code_input(
        message: Message,
        state: FSMContext,
        sale_repository: SaleRepository,
        salesman: Salesman,
        code: str,
) -> None:
    await state.clear()
    sale = await sale_repository.create(
        code=code,
        salesman_user_id=salesman.user_id,
    )
    view = SaleTemporaryCodeSuccessfullyAppliedView(sale)
    await answer_view(message, view)
