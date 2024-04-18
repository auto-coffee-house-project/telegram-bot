from uuid import UUID

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import ExceptionTypeFilter, StateFilter
from aiogram.types import ErrorEvent, Message

from exceptions import (
    InvitationDoesNotExistError,
    InvitationExpiredError,
    SalesmanAlreadyExistsError,
    UserIsAlreadyAdminError,
)
from filters import invitation_deeplink_filter
from repositories import EmployeeRepository
from views import EmployeeCreatedView, answer_view

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(UserIsAlreadyAdminError))
async def on_user_is_already_admin_error(event: ErrorEvent) -> None:
    await event.update.message.answer(f'❌ Вы уже являетесь администратором')


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
        salesman_repository: EmployeeRepository,
) -> None:
    salesman_created = await salesman_repository.create(
        invitation_id=invitation_id,
        user_id=message.from_user.id,
    )
    view = EmployeeCreatedView(salesman_created)
    await answer_view(message, view)
