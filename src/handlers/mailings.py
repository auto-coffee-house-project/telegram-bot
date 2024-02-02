from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters import user_is_admin_filter
from repositories import MailingRepository
from states import ShopMailingStates
from views import MailingConfirmView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == '📨 Рассылка',
    user_is_admin_filter,
    StateFilter('*'),
)
async def on_start_mailing(
        message: Message,
        state: FSMContext,
) -> None:
    await state.set_state(ShopMailingStates.text)
    await message.reply('✏️ Введите текст рассылки')


@router.message(
    F.text,
    user_is_admin_filter,
    StateFilter(ShopMailingStates.text),
)
async def on_mailing_message_input(
        message: Message,
        state: FSMContext,
) -> None:
    await state.set_state(ShopMailingStates.confirm)
    await state.update_data(text=message.html_text)
    view = MailingConfirmView(message.html_text)
    await answer_view(message, view)


@router.callback_query(
    F.data == 'mailing-confirm',
    user_is_admin_filter,
    StateFilter(ShopMailingStates.confirm),
)
async def on_mailing_confirm(
        callback_query: CallbackQuery,
        state: FSMContext,
        mailing_repository: MailingRepository,
        bot: Bot,
) -> None:
    state_data = await state.get_data()
    text: str = state_data['text']
    await mailing_repository.create(
        text=text,
        bot_id=bot.id,
        admin_user_id=callback_query.from_user.id,
    )
    await callback_query.message.edit_text('📨 Рассылка создана')
    await state.clear()


@router.callback_query(
    F.data == 'mailing-cancel',
    user_is_admin_filter,
    StateFilter('*'),
)
async def on_mailing_cancel(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await callback_query.answer(
        text='📨 Рассылка отменена',
        show_alert=True,
    )
    await callback_query.message.delete()
    await state.clear()
