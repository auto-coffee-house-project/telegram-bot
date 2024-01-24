from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from exceptions import AdminDoesNotExistError
from filters import admin_filter
from repositories import InvitationRepository, MailingRepository
from states import ShopMailingStates
from views import answer_view, MailingConfirmView, InvitationView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == '🔗 Ссылка-приглашение',
    StateFilter('*'),
)
async def on_create_invitation(
        message: Message,
        bot: Bot,
        invitation_repository: InvitationRepository,
) -> None:
    try:
        invitation = await invitation_repository.create(message.from_user.id)
    except AdminDoesNotExistError:
        await message.reply('Вы не являетесь администратором')
        return
    bot_user = await bot.get_me()
    view = InvitationView(bot_username=bot_user.username, invitation=invitation)
    await answer_view(message, view)


@router.message(
    F.text == '📨 Рассылка',
    admin_filter,
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
    StateFilter(ShopMailingStates.confirm),
)
async def on_mailing_confirm(
        callback_query: CallbackQuery,
        state: FSMContext,
        mailing_repository: MailingRepository,
) -> None:
    state_data = await state.get_data()
    text: str = state_data['text']
    await mailing_repository.create(
        text=text,
        admin_user_id=callback_query.from_user.id,
    )
    await callback_query.message.edit_text('📨 Рассылка создана')
    await state.clear()
