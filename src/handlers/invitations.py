from uuid import UUID

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter, ExceptionTypeFilter
from aiogram.types import Message, ErrorEvent

from exceptions import InvitationExpiredError, InvitationDoesNotExistError
from filters import invitation_deeplink_filter
from repositories import SalesmanRepository
from views import SalesmanCreatedView, answer_view

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
