from uuid import UUID

from aiogram import F, Bot, Router
from aiogram.enums import ChatType
from aiogram.filters import ExceptionTypeFilter, StateFilter
from aiogram.types import ErrorEvent, Message

from exceptions import (
    AdminDoesNotExistError,
    InvitationExpiredError,
    InvitationDoesNotExistError,
)
from filters import invitation_deeplink_filter, user_is_admin_filter
from repositories import InvitationRepository, SalesmanRepository
from views import SalesmanCreatedView, answer_view, InvitationView

router = Router(name=__name__)


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


@router.message(
    F.text == '🔗 Ссылка-приглашение',
    user_is_admin_filter,
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
