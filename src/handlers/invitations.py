from uuid import UUID

from aiogram import F, Bot, Router
from aiogram.enums import ChatType
from aiogram.filters import ExceptionTypeFilter, StateFilter
from aiogram.types import ErrorEvent, Message, CallbackQuery

from exceptions import (
    AdminDoesNotExistError,
    InvitationExpiredError,
    InvitationDoesNotExistError,
    SalesmanAlreadyExistsError,
)
from filters import invitation_deeplink_filter, user_is_admin_filter
from repositories import InvitationRepository, SalesmanRepository
from views import SalesmanCreatedView, answer_view, InvitationView, edit_view

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(SalesmanAlreadyExistsError))
async def on_salesman_already_exists_error(event: ErrorEvent) -> None:
    await event.update.message.answer(f'❌ Вы уже являетесь продавцом')


@router.error(ExceptionTypeFilter(InvitationExpiredError))
async def on_invitation_expired_error(event: ErrorEvent) -> None:
    await event.update.message.answer(f'❌ Срок действия пришлашения истек')


@router.error(ExceptionTypeFilter(InvitationDoesNotExistError))
async def on_invitation_does_not_exist_error(event: ErrorEvent) -> None:
    await event.update.message.answer(f'❌ Приглашение не найдено')


@router.message(
    F.chat.type == ChatType.PRIVATE,
    invitation_deeplink_filter,
    StateFilter('*'),
)
async def on_accept_invitation(
        message: Message,
        invitation_id: UUID,
        salesman_repository: SalesmanRepository,
) -> None:
    salesman_created = await salesman_repository.create(
        invitation_id=invitation_id,
        user_id=message.from_user.id,
    )
    view = SalesmanCreatedView(salesman_created)
    await answer_view(message, view)


@router.callback_query(
    F.data == 'add-salesman',
    user_is_admin_filter,
    StateFilter('*'),
)
async def on_create_invitation(
        callback_query: CallbackQuery,
        bot: Bot,
        invitation_repository: InvitationRepository,
) -> None:
    admin_user_id = callback_query.from_user.id
    try:
        invitation = await invitation_repository.create(admin_user_id)
    except AdminDoesNotExistError:
        await callback_query.answer(
            text='Вы не являетесь администратором',
            show_alert=True,
        )
        return
    bot_user = await bot.get_me()
    view = InvitationView(bot_username=bot_user.username, invitation=invitation)
    await edit_view(callback_query.message, view)
